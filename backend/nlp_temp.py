import spacy

nlp = spacy.load("en_core_web_sm")

def enrich_row_with_nlp(row: dict) -> dict:
    doc = nlp(row["item"])
    row["nlp_entities"] = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    try:
        prev = row["previous_price"]
        new = row["new_price"]
        percent_change = ((new - prev) / prev) * 100
        row["price_increase_percent"] = round(percent_change, 2)
    except ZeroDivisionError:
        row["price_increase_percent"] = None

    return row

def extract_price_table(text_lines: list) -> list:
    data = []
    rows = []
    buffer = []

    skip_words = {"id", "item", "name", "unit", "of", "issue", "previous", "price", "new"}

    for word in text_lines:
        if word.strip().lower() in skip_words:
            continue
        buffer.append(word.strip())
        if len(buffer) == 4:
            rows.append(buffer)
            buffer = []

    for i, row in enumerate(rows):
        try:
            item, unit, prev_price, new_price = row

            if item[0].isdigit():
                parts = item.split(" ", 1)
                item_id = int(parts[0])
                item_name = parts[1] if len(parts) > 1 else ""
            else:
                item_id = i + 1
                item_name = item

            row_data = {
                "id": item_id,
                "item": item_name,
                "unit": unit,
                "previous_price": float(prev_price),
                "new_price": float(new_price)
            }

            row_data = enrich_row_with_nlp(row_data)
            data.append(row_data)

        except Exception as e:
            print(f"Skipping bad row {row} due to error: {e}")

    return data
