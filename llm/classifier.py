import json
from ollama import chat

CATEGORIES = [
    "Antibiotic",
    "Antiviral",
    "Antifungal",
    "Analgesic",
    "Antidiabetic",
    "Antihypertensive",
    "Antacid",
    "Vitamin",
    "Supplement",
    "Cardiovascular",
    "Respiratory",
    "Antidepressant",
    "Antipsychotic",
    "Corticosteroid"
]


def classify_item(item_name: str):

    prompt = f"""
You are a pharmaceutical inventory validator.

Task:

1. Determine if the item is a medicine.
2. If it is a medicine:
   - Correct any spelling mistakes.
   - Classify it into EXACTLY ONE category from:

{", ".join(CATEGORIES)}

3. If it is NOT a medicine:
   - Explain why.

Return ONLY valid JSON.

Medicine Name:
{item_name}

Examples:

{{
  "is_medicine": true,
  "suggested_name": "Paracetamol",
  "category": "Analgesic",
  "confidence": 0.98,
  "reason": null
}}

{{
  "is_medicine": false,
  "suggested_name": "Laptop",
  "category": null,
  "confidence": 1.0,
  "reason": "Laptop is an electronic device and not a medicine."
}}
"""

    response = chat(
        model="gpt-oss:120b-cloud",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    return json.loads(text)