import os
import json
import easyocr
import cv2
import numpy as np
from pdf2image import convert_from_path
from pathlib import Path

# Initialize OCR reader once
reader = easyocr.Reader(['en'], gpu=False)

# ========= PDF OCR Function =========
def process_pdf(pdf_path, output_json_path):
    print(f"Processing PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=300)
    output_data = []

    for i, page in enumerate(pages):
        img = np.array(page)
        results = reader.readtext(img)
        page_texts = [text for (_, text, _) in results]

        output_data.append({
            "page_number": i + 1,
            "text": page_texts
        })

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)

    print(f"PDF OCR saved to '{output_json_path}'")

# ========= Image OCR Function =========
def process_image(image_path, output_json_path):
    print(f"Processing Image: {image_path}")
    img = cv2.imread(image_path)
    results = reader.readtext(img)
    image_texts = [text for (_, text, _) in results]

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding='utf-8') as f:
        json.dump({
            "image_file": os.path.basename(image_path),
            "text": image_texts
        }, f, indent=4)

    print(f"Image OCR saved to '{output_json_path}'")


# if __name__ == "__main__":

#     # PDFs
#     # pdf_path = 'pdfs/Deposits.pdf'
#     # pdf_output = 'output/pdf_ocr_output.json'
#     # process_pdf(pdf_path, pdf_output)
    
#     pdf_path = 'backend/pdfs/PricingUpdate.pdf'
#     pdf_output = 'backend/output/pdf_ocr_output.json'
#     process_pdf(pdf_path, pdf_output)

#     # Images
#     # image_path = 'images/PC.png'
#     # image_output = 'output/image_ocr_output.json'
#     # process_image(image_path, image_output)
    
#     image_path = 'backend/images/PricingUpdate.png'
#     image_output = 'backend/output/image_ocr_output.json'
#     process_image(image_path, image_output)
