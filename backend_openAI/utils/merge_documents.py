from collections import defaultdict

def merge_documents_by_key(structured_data, key):
    """
    Merge document parts (e.g., multi-page invoices or quotes) by a shared key like invoice_number, quote_number, po_number, order_number, etc..
    Each item in structured_data is a page result.
    """
    merged_map = defaultdict(lambda: {
        key: None,
        "date": None,
        "vendor": None,
        "items": [],
        "subtotal": 0.0,
        "tax": 0.0,
        "grand_total": 0.0
    })

    for page in structured_data:
        for doc in page:
            doc_key = doc.get(key)
            if not doc_key:
                continue  # Skip if key is missing

            merged = merged_map[doc_key]

            if not merged[key]:
                merged[key] = doc_key
                merged["date"] = doc.get("date")
                merged["vendor"] = doc.get("vendor")

            merged["items"].extend(doc.get("items", []))

            # Prefer latest non-zero values (likely from last page)
            for field in ["subtotal", "tax", "grand_total"]:
                val = doc.get(field)
                if val and isinstance(val, (int, float)) and val > 0:
                    merged[field] = val

    return list(merged_map.values())
