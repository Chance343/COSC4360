import pandas as pd
import numpy as np
from io import BytesIO
import json
import os
from datetime import datetime
from fastapi.responses import JSONResponse


def process_csv(contents, doc_type, filename):
    df = pd.read_csv(BytesIO(contents))

    # Clean headers
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Replace bad values with None
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

    structured_data = df.to_dict(orient="records")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "doc_type": doc_type,
        "filename": filename,
        "timestamp": timestamp,
        "structured_data": structured_data,
    }

    os.makedirs("output", exist_ok=True)
    with open(f"output/{doc_type}_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, allow_nan=False)

    return JSONResponse(content=output)


def process_excel(contents, doc_type, filename):
    df = pd.read_excel(BytesIO(contents), engine="openpyxl")

    # Normalize headers
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Replace NaN, inf, -inf with None (safe for JSON)
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})

    structured_data = df.to_dict(orient="records")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = {
        "doc_type": doc_type,
        "filename": filename,
        "timestamp": timestamp,
        "structured_data": structured_data,
    }

    os.makedirs("output", exist_ok=True)
    with open(f"output/{doc_type}_{timestamp}.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4, allow_nan=False)

    return JSONResponse(content=output)