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
import pandas as pd

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
            df = pd.read_csv(BytesIO(contents))
            structured_data = df.to_dict(orient="records")

            # ✅ Normalize header keys
            for i, row in enumerate(structured_data):
                structured_data[i] = {k.strip().lower(): v for k, v in row.items()}

            structured_data = [structured_data]  # Wrap for consistency

        # === Excel ===
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(BytesIO(contents), engine="openpyxl")
            structured_data = [df.to_dict(orient="records")]
            
        else:
            # Regular image handling (PNG, JPEG, etc.)
            base64_image = base64.b64encode(contents).decode("utf-8")
            data_url = f"data:{file.content_type};base64,{base64_image}"
            structured_data = extract_json_from_vision(data_url, prompt)


        # else:
        #     return JSONResponse(status_code=400, content={"error": "Unsupported file type"})
        

        if doc_type == "vendor_invoice":
            # Ensure page-wise structure for CSV/Excel (flat list → list of pages)
            if structured_data and isinstance(structured_data[0], dict):
                structured_data = [structured_data]

            # Alias common invoice field names to "invoice_number"
            COMMON_INVOICE_KEYS = ["invoice", "invoice no", "invoice#", "invoice_num"]
            for page in structured_data:
                for entry in page:
                    for alt_key in COMMON_INVOICE_KEYS:
                        if alt_key in entry and "invoice_number" not in entry:
                            entry["invoice_number"] = entry.pop(alt_key)

            # Validate key presence before merging
            if not all("invoice_number" in entry for page in structured_data for entry in page):
                return JSONResponse(status_code=400, content={
                    "error": "Missing 'invoice_number' in one or more rows of the uploaded file."
                })

            # Now safe to merge
            structured_data = merge_documents_by_key(structured_data, key="invoice_number")

        elif doc_type == "supply_quote":
            # Step 1: Alias fields
            for page in structured_data:
                for entry in page:
                    if "quote_number" in entry and "invoice_number" not in entry:
                        entry["invoice_number"] = entry.pop("quote_number")
                    if "total_value" in entry and "grand_total" not in entry:
                        entry["grand_total"] = entry.pop("total_value")

            # Step 1.5: Validate all entries have the invoice_number
            if not all("invoice_number" in entry for page in structured_data for entry in page):
                return JSONResponse(status_code=400, content={"error": "Missing 'quote_number' or improperly formatted CSV rows."})

            # Step 2: Merge
            structured_data = merge_documents_by_key(structured_data, key="invoice_number")

            # Step 3: Rename fields back
            for entry in structured_data:
                entry["quote_number"] = entry.pop("invoice_number", None)
                entry["total_value"] = entry.pop("grand_total", None)


        elif doc_type == "supply_pricing_update":
            structured_data = structured_data  # No merge needed, already flat
            
        elif doc_type == "shipping_update":
            structured_data = structured_data[-1] if isinstance(structured_data, list) else structured_data

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
