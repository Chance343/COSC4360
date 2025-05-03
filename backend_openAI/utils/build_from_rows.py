from collections import defaultdict

def build_from_rows(rows, invoice_key="invoice_number"):
    grouped = defaultdict(lambda: {
        "invoice_number": None,
        "date": None,
        "vendor": None,
        "items": [],
        "subtotal": 0,
        "tax": 0,
        "grand_total": 0
    })

    for row in rows:
        row = {k.strip().lower(): v for k, v in row.items()}
        inv_id = row.get(invoice_key)
        if not inv_id:
            continue

        inv = grouped[inv_id]
        inv["invoice_number"] = inv_id
        inv["date"] = inv["date"] or row.get("date")
        inv["vendor"] = inv["vendor"] or row.get("vendor")

        # Detect if this is a line item or summary row
        if row.get("item") or row.get("description"):
            item = {
                "description": row.get("item") or row.get("description"),
                "qty": row.get("qty") or row.get("quantity"),
                "unit_price": row.get("unit_price"),
                "total": row.get("total")
            }
            inv["items"].append(item)

        # Set totals from any row that has them
        inv["subtotal"] = row.get("subtotal") or inv["subtotal"]
        inv["tax"] = row.get("tax") or inv["tax"]
        inv["grand_total"] = row.get("grand_total") or row.get("total_value") or inv["grand_total"]

    return list(grouped.values())
