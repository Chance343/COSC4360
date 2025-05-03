# prompt_factory.py
def get_prompt_for(doc_type: str) -> str:
    if doc_type == "supply_pricing_update":
        return (
            "You are reading a supply pricing update document. Extract all rows in the pricing table.\n\n"
            "Each row should include:\n"
            "- item name\n"
            "- unit (e.g., dozen, lb, ft)\n"
            "- previous_price (number)\n"
            "- new_price (number)\n\n"
            "Return a JSON array in this format:\n"
            "[\n"
            "  {\n"
            "    \"id\": 1,\n"
            "    \"item\": \"Eggs\",\n"
            "    \"unit\": \"dozen\",\n"
            "    \"previous_price\": 1.99,\n"
            "    \"new_price\": 2.30\n"
            "  }\n"
            "]\n\n"
            "Respond only with valid JSON. Do not include explanations or markdown code blocks."
        )
    elif doc_type == "supply_quote":
        return (
            "You are analyzing a multi-page supply quote document. Pages may contain one or more full or partial quotes.\n\n"
            "Group all pages together and merge line items that share the same quote_number.\n"
            "Return exactly one quote object per quote_number.\n\n"
            "For each quote, extract:\n"
            "- quote_number\n"
            "- date\n"
            "- vendor\n"
            "- items (each with: item, quantity, unit, unit_price, total)\n"
            "- subtotal\n"
            "- tax\n"
            "- total_value\n\n"
            "Return a **JSON array** of quotes like this:\n"
            "[\n"
            "  {\n"
            "    \"quote_number\": \"Q123456\",\n"
            "    \"date\": \"2025-03-21\",\n"
            "    \"vendor\": \"Mountainland Supply Company\",\n"
            "    \"items\": [\n"
            "      { \"item\": \"item A\", \"quantity\": 2, \"unit\": \"ea\", \"unit_price\": 12.34, \"total\": 24.68 },\n"
            "      { \"item\": \"item B\", \"quantity\": 3, \"unit\": \"ea\", \"unit_price\": 5.00, \"total\": 15.00 }\n"
            "    ],\n"
            "    \"subtotal\": 39.68,\n"
            "    \"tax\": 2.32,\n"
            "    \"total_value\": 42.00\n"
            "  }\n"
            "]\n\n"
            "Respond only with valid JSON. Do not include explanations or markdown."
        )



    elif doc_type == "shipping_update":
        return (
            "You are analyzing a shipping update document. Extract shipment details and item list.\n\n"
            "Include the following fields:\n"
            "- shipment_id\n"
            "- carrier\n"
            "- origin\n"
            "- destination\n"
            "- estimated_arrival_date\n"
            "- items: a list of objects, each with `description` and `quantity`\n\n"
            "Return a single JSON object in this format:\n"
            "{\n"
            "  \"shipment_id\": \"SH123456\",\n"
            "  \"carrier\": \"UPS\",\n"
            "  \"origin\": \"Dallas, TX\",\n"
            "  \"destination\": \"Austin, TX\",\n"
            "  \"estimated_arrival_date\": \"2024-05-01\",\n"
            "  \"items\": [\n"
            "    { \"description\": \"Water Heater\", \"quantity\": 2 },\n"
            "    { \"description\": \"Brass Fittings\", \"quantity\": 10 }\n"
            "  ]\n"
            "}\n\n"
            "Respond only with JSON. Do not include explanations or markdown."
        )

    elif doc_type == "vendor_invoice":
        return (
            "You are analyzing a multi-page invoice document. Pages may contain one or more full or partial invoices.\n\n"
            "Group all pages together and merge line items that share the same invoice_number.\n"
            "Return exactly one invoice object per invoice_number.\n\n"
            "For each invoice, extract:\n"
            "- invoice_number\n"
            "- date\n"
            "- vendor\n"
            "- items (each with: description, qty, unit_price, total)\n"
            "- subtotal\n"
            "- tax\n"
            "- grand_total\n\n"
            "Return a **JSON array** of invoices like this:\n"
            "[\n"
            "  {\n"
            "    \"invoice_number\": \"S10690577.001\",\n"
            "    \"date\": \"2025-03-21\",\n"
            "    \"vendor\": \"Mountainland Supply Company\",\n"
            "    \"items\": [\n"
            "      { \"description\": \"item A\", \"qty\": 2, \"unit_price\": 12.34, \"total\": 24.68 },\n"
            "      { \"description\": \"item B\", \"qty\": 3, \"unit_price\": 5.00, \"total\": 15.00 }\n"
            "    ],\n"
            "    \"subtotal\": 39.68,\n"
            "    \"tax\": 2.32,\n"
            "    \"grand_total\": 42.00\n"
            "  }\n"
            "]\n\n"
            "Respond only with JSON. Do not include explanations or markdown code blocks."
        )


    else:
        raise ValueError(f"Unsupported document type: {doc_type}")
