# vision_extractor.py
import json
import re
from openai import OpenAI

client = OpenAI()

def extract_json_from_vision(data_url: str, prompt: str) -> dict:
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
