# main.py
import os
import base64
import json
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prompt_factory import get_prompt_for
from vision_extractor import extract_json_from_vision
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image
import pandas as pd

from db import insert_into_table, fetch_from_table
from utils.merge_documents import merge_documents_by_key
from utils.build_from_rows import build_from_rows
from utils.file_parsers import process_csv, process_excel
from utils.document_merger import handle_merging_logic


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# POST - http://127.0.0.1:8000/upload/vendor_invoice
@app.post("/upload/{doc_type}")
async def upload_file(doc_type: str, file: UploadFile = File(...)):
    try:
        prompt = get_prompt_for(doc_type)
        contents = await file.read()
        structured_data = []
            
        # # === PDF/Images ===
        if file.content_type == "application/pdf":
            # Convert each page of PDF to image
            images = convert_from_bytes(contents, dpi=300)
            for img in images:
                buf = BytesIO()
                img.save(buf, format="PNG")
                base64_image = base64.b64encode(buf.getvalue()).decode("utf-8")
                data_url = f"data:image/png;base64,{base64_image}"
                extracted = extract_json_from_vision(data_url, prompt)
                structured_data.append(extracted)

        # === CSV ===
        elif file.filename.endswith(".csv"):
            return process_csv(contents, doc_type, file.filename)

        # === Excel ===
        elif file.filename.endswith(".xlsx"):
            return process_excel(contents, doc_type, file.filename)

        # === Regular image (e.g., PNG/JPEG) ===
        else:
            base64_image = base64.b64encode(contents).decode("utf-8")
            data_url = f"data:{file.content_type};base64,{base64_image}"
            structured_data = extract_json_from_vision(data_url, prompt)        
        
        # === Document-type-specific merging/normalization ===
        structured_data = handle_merging_logic(doc_type, structured_data)
        
        # === Final output formatting ===
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = {
            "doc_type": doc_type,
            "filename": file.filename,
            "timestamp": timestamp,
            "structured_data": structured_data,
        }
        # inserting uploaded data into table
        insert_into_table(file.filename, file.size, timestamp, doc_type, structured_data)

        os.makedirs("output", exist_ok=True)
        with open(f"output/{doc_type}_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        return JSONResponse(content=output)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# GET - http://127.0.0.1:8000/get
@app.get("/get")
async def get_documents():
    try:
        # fetching uploaded data from table
        documents = fetch_from_table()

        return JSONResponse(content=documents)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
