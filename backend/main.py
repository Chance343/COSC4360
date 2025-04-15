from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
import logging
import json

from ocr_processor import process_pdf, process_image
from nlp_temp import extract_price_table

from nlp_processor import process_ocr_text

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Allow all CORS origins for testing — you can restrict this later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    logging.info(f"Received file: {filename}")
    suffix = Path(filename).suffix.lower()
    temp_file_path = f"temp/{uuid.uuid4()}{suffix}"

    contents = await file.read()

    logging.info(f"Content type: {file.content_type}")
    logging.info(f"File size: {len(contents)} bytes")

    # Save the uploaded file
    Path("temp").mkdir(exist_ok=True)
    with open(temp_file_path, "wb") as buffer:
        buffer.write(contents)

    # Decide how to process
    output_path = f"output/{Path(filename).stem}_ocr.json"
    Path("output").mkdir(exist_ok=True)

    if suffix == ".pdf":
        process_pdf(temp_file_path, output_path)
    elif suffix in [".png", ".jpg", ".jpeg"]:
        process_image(temp_file_path, output_path)
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    # # Return the result
    # with open(output_json_path, "r", encoding="utf-8") as f:
    #     result = f.read()
        
    # # Parse JSON text into a Python dictionary/list
    # ocr_data = json.loads(result)
    
    with open(output_path, "r") as f:
        ocr_data = json.load(f)
        
    # Prepare text for NLP
    if isinstance(ocr_data, dict) and "text" in ocr_data:
        full_text = " ".join(ocr_data["text"])
    elif isinstance(ocr_data, list):  # PDF case
        all_text = []
        for page in ocr_data:
            all_text.extend(page.get("text", []))
        full_text = " ".join(all_text)
    else:
        full_text = ""

    # Run NLP processing
    # structured_data = process_ocr_text(full_text)
    
    structured_data = extract_price_table(ocr_data.get("text", []))
        
    # with open("output/nlp_output.json", "w", encoding="utf-8") as f:
    #     json.dump(structured_data, f, indent=4)
    with open("output/nlp_output.json", "w", encoding="utf-8") as f:
        json.dump(structured_data, f, indent=4)

    logging.info("NLP process complete")

    
    # return JSONResponse(content={
    #     "filename": filename,
    #     "ocr_text": full_text,
    #     "structured_data": structured_data
    # })
    return JSONResponse(content={
        "filename": filename,
        "structured_data": structured_data
    })

    # return JSONResponse(content={"filename": filename, "ocr_result": result})