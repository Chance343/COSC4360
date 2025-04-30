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
            "You are reading a supply quote document. Extract all quoted items with pricing details.\n\n"
            "Each item should include:\n"
            "- item name\n"
            "- quantity\n"
            "- unit (e.g., pcs, ft, lb)\n"
            "- unit_price (number)\n"
            "- total (number)\n\n"
            "Return a JSON array in this format:\n"
            "[\n"
            "  {\n"
            "    \"item\": \"Steel Rod\",\n"
            "    \"quantity\": 100,\n"
            "    \"unit\": \"pcs\",\n"
            "    \"unit_price\": 5.50,\n"
            "    \"total\": 550.00\n"
            "  }\n"
            "]\n\n"
            "Respond only with valid JSON. No text or markdown outside the JSON block."
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
            "You are analyzing a multi-page invoice document. Each page may contain one or more full or partial invoices.\n\n"
            "Extract data for each invoice that appears on this page. For each invoice, include:\n"
            "- invoice_number\n"
            "- date\n"
            "- vendor\n"
            "- items (each with: description, qty, unit_price, total)\n"
            "- grand_total\n\n"
            "If a page continues a previously listed invoice (same invoice_number), include only new `items`.\n"
            "Do not repeat the vendor, date, or grand_total fields for continuation pages.\n"
            "If nothing new appears on the page, return an empty array.\n\n"
            "Return a **JSON array** of invoices like this:\n"
            "[\n"
            "  {\n"
            "    \"invoice_number\": \"S10690577.001\",\n"
            "    \"items\": [\n"
            "      { \"description\": \"item A\", \"qty\": 2, \"unit_price\": 12.34, \"total\": 24.68 }\n"
            "    ]\n"
            "  }\n"
            "]\n\n"
            "Respond only with JSON. Do not include explanations or markdown code blocks."
        )
    else:
        raise ValueError(f"Unsupported document type: {doc_type}")
