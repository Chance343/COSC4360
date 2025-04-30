import json
import re
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def extract_json_from_vision(data_url: str, prompt: str) -> dict:
    # ✅ Create the OpenAI client INSIDE the function after loading .env
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.0,
    )

    reply = response.choices[0].message.content

    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        match = re.search(r'```(?:json)?\n(.*?)```', reply, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        raise Exception("Failed to parse JSON from GPT response.")
