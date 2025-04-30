# import os
# import json
# import base64
# from datetime import datetime
# from dotenv import load_dotenv
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from openai import OpenAI

# # Load environment variables from .env file
# load_dotenv()

# # Initialize OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Initialize FastAPI app
# app = FastAPI()

# # Allow frontend access (adjust origins as needed)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         mime_type = file.content_type

#         # Convert file to base64 for GPT vision
#         base64_image = base64.b64encode(contents).decode("utf-8")
#         data_url = f"data:{mime_type};base64,{base64_image}"

#         # Compose prompt for GPT-4 Vision
#         messages = [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": (
#                             "Extract the price update table from this image.\n\n"
#                             "Return only a JSON list in this format:\n"
#                             "[\n"
#                             "  {\n"
#                             "    \"id\": 1,\n"
#                             "    \"item\": \"Eggs\",\n"
#                             "    \"unit\": \"dozen\",\n"
#                             "    \"previous_price\": 1.99,\n"
#                             "    \"new_price\": 2.30\n"
#                             "  }\n"
#                             "]\n\n"
#                             "Do not include markdown or explanations."
#                         ),
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": data_url
#                         },
#                     },
#                 ],
#             }
#         ]

#         # Call OpenAI API
#         response = client.chat.completions.create(
#             model="gpt-4-turbo",
#             messages=messages,
#             temperature=0.0,
#         )

#         reply = response.choices[0].message.content

#         # Try parsing the reply into JSON
#         try:
#             structured_data = json.loads(reply)
#         except json.JSONDecodeError:
#             import re
#             match = re.search(r'```(?:json)?\n(.*?)```', reply, re.DOTALL)
#             if match:
#                 structured_data = json.loads(match.group(1))
#             else:
#                 raise Exception("Failed to parse JSON from GPT response.")

#         # Save to local output folder
#         os.makedirs("output", exist_ok=True)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         output_file = f"output/structured_data_{timestamp}.json"

#         with open(output_file, "w", encoding="utf-8") as f:
#             json.dump(structured_data, f, indent=4)

#         # Return JSON response
#         return JSONResponse(content={"structured_data": structured_data})

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})



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
        # Validate doc_type and fetch prompt
        prompt = get_prompt_for(doc_type)

        # Read file and encode as base64
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")
        data_url = f"data:{file.content_type};base64,{base64_image}"

        # Extract structured data
        structured_data = extract_json_from_vision(data_url, prompt)

        # Save result with metadata
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
