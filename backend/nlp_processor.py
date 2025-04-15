import re
import spacy

nlp = spacy.load("en_core_web_sm")

# ========== Rule-Based Extraction ==========

def extract_invoice_fields(text: str) -> dict:
    """
    Extracts key fields using regular expressions.
    Customize based on your document structure.
    """
    data = {}

    invoice_no_match = re.search(r"Invoice\s*(No\.?|#)?\s*[:\-]?\s*([A-Z0-9\-]+)", text, re.I)
    date_match = re.search(r"Date\s*[:\-]?\s*(\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4})", text)
    total_match = re.search(r"Total\s*Amount\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})", text, re.I)

    if invoice_no_match:
        data["invoice_number"] = invoice_no_match.group(2)
    if date_match:
        data["date"] = date_match.group(1)
    if total_match:
        data["total"] = total_match.group(1)

    return data

# ========== spaCy-Based Entity Extraction ==========

def extract_entities_spacy(text: str):
    """
    Uses spaCy to extract named entities from text.
    Not specific to invoices, but helpful for names, dates, orgs, etc.
    """
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

# ========== Combined Structured Output ==========

def process_ocr_text(text: str) -> dict:
    """
    Processes OCR text and returns structured data using both methods.
    """
    return {
        "rule_based": extract_invoice_fields(text),
        "spacy_entities": extract_entities_spacy(text)
    }
