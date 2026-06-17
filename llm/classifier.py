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


def classify_medicine(medicine_name: str):

    prompt = f"""
Classify the medicine into exactly one category.

Allowed categories:
{", ".join(CATEGORIES)}

Medicine:
{medicine_name}

Return ONLY valid JSON:

{{
  "category": "Antibiotic",
  "confidence": 0.98
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