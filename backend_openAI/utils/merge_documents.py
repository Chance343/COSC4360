from copy import deepcopy

def merge_documents_by_key(doc_type: str, pages: list) -> list:
    if doc_type == "vendor_invoice":
        key = "invoice_number"
        merge_fields = ["vendor", "date", "grand_total"]
    elif doc_type == "supply_quote":
        key = "quote_number"
        merge_fields = ["date", "vendor", "grand_total"]
    elif doc_type == "supply_pricing_update":
        key = "item"  # Or use item ID if you have one
        return _flatten_list_of_dicts(pages)
    elif doc_type == "shipping_update":
        key = "shipment_id"
        merge_fields = ["carrier", "origin", "destination", "estimated_arrival_date"]
    else:
        return _flatten_list_of_dicts(pages)

    # Merge grouped by key
    merged = {}
    all_entries = [entry for page in pages for entry in page]

    for entry in all_entries:
        entry_id = entry.get(key)
        if not entry_id:
            continue

        if entry_id not in merged:
            merged[entry_id] = deepcopy(entry)
        else:
            existing = merged[entry_id]
            existing["items"].extend(entry.get("items", []))

            for field in merge_fields:
                if not existing.get(field) and entry.get(field):
                    existing[field] = entry[field]

    return list(merged.values())

def _flatten_list_of_dicts(nested_list):
    return [entry for sublist in nested_list for entry in sublist]
