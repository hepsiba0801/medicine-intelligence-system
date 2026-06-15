import joblib

model = joblib.load("ml/category_model.joblib")
vectorizer = joblib.load("ml/category_vectorizer.joblib")


def predict_category(medicine_name):

    X = vectorizer.transform([medicine_name])

    category = model.predict(X)[0]

    confidence = float(
        model.predict_proba(X).max()
    )

    return {
        "category": category,
        "confidence": round(confidence, 4)
    }

print(predict_category("Paracetamol"))
print(predict_category("Metformin"))
print(predict_category("Cetirizine"))
print(predict_category("Amoxicillin"))
print(predict_category("Ibuprofen"))
print(predict_category("Aspirin"))
print(predict_category("Omeprazole"))
print(predict_category("Fluconazole"))
print(predict_category("Acyclovir"))
print(predict_category("Vitamin C"))