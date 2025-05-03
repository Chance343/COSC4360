# utils/document_mergers.py

from fastapi.responses import JSONResponse
from utils.merge_documents import merge_documents_by_key

def handle_merging_logic(doc_type, structured_data):
    if doc_type == "vendor_invoice":
        if structured_data and isinstance(structured_data[0], dict):
            structured_data = [structured_data]

        COMMON_INVOICE_KEYS = ["invoice", "invoice no", "invoice#", "invoice_num"]
        for page in structured_data:
            for entry in page:
                for alt_key in COMMON_INVOICE_KEYS:
                    if alt_key in entry and "invoice_number" not in entry:
                        entry["invoice_number"] = entry.pop(alt_key)

        if not all("invoice_number" in entry for page in structured_data for entry in page):
            return JSONResponse(status_code=400, content={
                "error": "Missing 'invoice_number' in one or more rows of the uploaded file."
            })

        return merge_documents_by_key(structured_data, key="invoice_number")

    elif doc_type == "supply_quote":
        if structured_data and isinstance(structured_data[0], dict):
            structured_data = [structured_data]

        COMMON_QUOTE_KEYS = ["quote", "quote no", "quote#", "estimate"]
        for page in structured_data:
            for entry in page:
                for alt_key in COMMON_QUOTE_KEYS:
                    if alt_key in entry and "quote_number" not in entry:
                        entry["quote_number"] = entry.pop(alt_key)

                if "total_value" not in entry and "grand_total" in entry:
                    entry["total_value"] = entry.pop("grand_total")

                entry["invoice_number"] = entry.get("quote_number")
                entry["grand_total"] = entry.get("total_value", 0.0)
                entry["items"] = entry.get("items", [])
                entry["date"] = entry.get("date")
                entry["vendor"] = entry.get("vendor")

        if not all("invoice_number" in entry for page in structured_data for entry in page):
            return JSONResponse(status_code=400, content={
                "error": "Missing 'quote_number' or alias in one or more rows of the uploaded file."
            })

        structured_data = merge_documents_by_key(structured_data, key="invoice_number")

        for entry in structured_data:
            entry["quote_number"] = entry.pop("invoice_number")
            entry["total_value"] = entry.pop("grand_total")

        return structured_data

    elif doc_type == "supply_pricing_update":
        return structured_data

    elif doc_type == "shipping_update":
        return structured_data[-1] if isinstance(structured_data, list) else structured_data

    return structured_data




        # if doc_type == "vendor_invoice":
        #     # Ensure page-wise structure for CSV/Excel (flat list → list of pages)
        #     if structured_data and isinstance(structured_data[0], dict):
        #         structured_data = [structured_data]

        #     # Alias common invoice field names to "invoice_number"
        #     COMMON_INVOICE_KEYS = ["invoice", "invoice no", "invoice#", "invoice_num"]
        #     for page in structured_data:
        #         for entry in page:
        #             for alt_key in COMMON_INVOICE_KEYS:
        #                 if alt_key in entry and "invoice_number" not in entry:
        #                     entry["invoice_number"] = entry.pop(alt_key)

        #     # Validate key presence before merging
        #     if not all("invoice_number" in entry for page in structured_data for entry in page):
        #         return JSONResponse(status_code=400, content={
        #             "error": "Missing 'invoice_number' in one or more rows of the uploaded file."
        #         })

        #     # Now safe to merge
        #     structured_data = merge_documents_by_key(structured_data, key="invoice_number")
            
        # elif doc_type == "supply_quote":
        #     # Ensure page-wise structure for CSV/Excel (flat list → list of pages)
        #     if structured_data and isinstance(structured_data[0], dict):
        #         structured_data = [structured_data]

        #     # Alias common quote field names to "quote_number"
        #     COMMON_QUOTE_KEYS = ["quote", "quote no", "quote#", "estimate"]
        #     for page in structured_data:
        #         for entry in page:
        #             for alt_key in COMMON_QUOTE_KEYS:
        #                 if alt_key in entry and "quote_number" not in entry:
        #                     entry["quote_number"] = entry.pop(alt_key)

        #             # Normalize total field for merging logic
        #             if "total_value" not in entry and "grand_total" in entry:
        #                 entry["total_value"] = entry.pop("grand_total")

        #             # Alias for merging
        #             entry["invoice_number"] = entry.get("quote_number")
        #             entry["grand_total"] = entry.get("total_value", 0.0)
        #             entry["items"] = entry.get("items", [])
        #             entry["date"] = entry.get("date")
        #             entry["vendor"] = entry.get("vendor")

        #     # Validate key presence
        #     if not all("invoice_number" in entry for page in structured_data for entry in page):
        #         return JSONResponse(status_code=400, content={
        #             "error": "Missing 'quote_number' or alias in one or more rows of the uploaded file."
        #         })

        #     # Merge using invoice_number logic
        #     structured_data = merge_documents_by_key(structured_data, key="invoice_number")

        #     # Revert key names after merging
        #     for entry in structured_data:
        #         entry["quote_number"] = entry.pop("invoice_number")
        #         entry["total_value"] = entry.pop("grand_total")



        # elif doc_type == "supply_pricing_update":
        #     structured_data = structured_data  # No merge needed, already flat
            
        # elif doc_type == "shipping_update":
        #     structured_data = structured_data[-1] if isinstance(structured_data, list) else structured_data
        