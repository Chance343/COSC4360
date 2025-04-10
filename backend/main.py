from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import uuid
from ocr_processor import process_pdf, process_image

app = FastAPI()

# Enable CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust if frontend runs on another port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    suffix = Path(filename).suffix.lower()
    temp_file_path = f"temp/{uuid.uuid4()}{suffix}"

    # Save the uploaded file
    Path("temp").mkdir(exist_ok=True)
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Decide how to process
    output_json_path = f"output/{Path(filename).stem}_ocr.json"
    Path("output").mkdir(exist_ok=True)

    if suffix == ".pdf":
        process_pdf(temp_file_path, output_json_path)
    elif suffix in [".png", ".jpg", ".jpeg"]:
        process_image(temp_file_path, output_json_path)
    else:
        return JSONResponse(content={"error": "Unsupported file type"}, status_code=400)

    # Return the result
    with open(output_json_path, "r", encoding="utf-8") as f:
        result = f.read()

    return JSONResponse(content={"filename": filename, "ocr_result": result})
