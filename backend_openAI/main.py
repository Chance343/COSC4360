# main.py
import os
import base64
import json
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prompt_factory import get_prompt_for
from vision_extractor import extract_json_from_vision
from pdf2image import convert_from_bytes
from io import BytesIO
from PIL import Image  # Needed to validate images

from utils.merge_documents import merge_documents_by_key


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/{doc_type}")
async def upload_file(doc_type: str, file: UploadFile = File(...)):
    try:
        prompt = get_prompt_for(doc_type)
        contents = await file.read()
        structured_data = []

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
        else:
            # Regular image handling (PNG, JPEG, etc.)
            base64_image = base64.b64encode(contents).decode("utf-8")
            data_url = f"data:{file.content_type};base64,{base64_image}"
            structured_data = extract_json_from_vision(data_url, prompt)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = {
            "doc_type": doc_type,
            "filename": file.filename,
            "timestamp": timestamp,
            "structured_data": structured_data,
        }

        os.makedirs("output", exist_ok=True)
        with open(f"output/{doc_type}_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4)

        return JSONResponse(content=output)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})