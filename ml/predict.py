import joblib
model = joblib.load("ml/model.joblib")


def predict_medicine(name: str):

    prediction = model.predict([name])[0]

    if prediction == 1:
        return "Medicine"

    return "Not Medicine"

print(predict_medicine("Paracetamol"))
print(predict_medicine("Apple"))
print(predict_medicine("Aspirin"))
print(predict_medicine("samsung"))
print(predict_medicine("he"))
print(predict_medicine("hallo"))
print(predict_medicine("Metfornin"))
print(predict_medicine("Dolo"))