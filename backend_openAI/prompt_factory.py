# prompt_factory.py
def get_prompt_for(doc_type: str) -> str:
    if doc_type == "supply_pricing_update":
        return (
            "Extract the price update table from this image.\n\n"
            "Return only a JSON list in this format:\n"
            "[{ \"id\": 1, \"item\": \"Eggs\", \"unit\": \"dozen\", \"previous_price\": 1.99, \"new_price\": 2.30 }]"
            "\n\nDo not include markdown or explanations."
        )
    elif doc_type == "supply_quote":
        return (
            "Extract supply quote data from this document including item name, quantity, unit, price per unit, and total.\n\n"
            "Return only JSON in this format:\n"
            "[{ \"item\": \"Steel Rod\", \"quantity\": 100, \"unit\": \"pcs\", \"unit_price\": 5.50, \"total\": 550.00 }]"
        )
    elif doc_type == "shipping_update":
        return (
            "Extract the shipping update details including shipment ID, carrier, origin, destination, estimated arrival date, and items with quantity.\n\n"
            "Return only JSON."
        )
    elif doc_type == "vendor_invoice":
        return (
            "Extract invoice data including invoice number, date, vendor name, items (description, qty, unit price, total), and grand total.\n\n"
            "Return only JSON in this format:\n"
            "{ \"invoice_number\": \"INV-12345\", \"date\": \"2024-04-15\", \"vendor\": \"ABC Corp\", \"items\": [...], \"grand_total\": 1234.56 }"
        )
    else:
        raise ValueError(f"Unsupported document type: {doc_type}")
