import joblib

model = joblib.load("ml/model.joblib")


def predict_medicine(name: str):

    prediction = model.predict([name])[0]

    confidence = max(
        model.predict_proba([name])[0]
    )

    confidence = round(
        float(confidence),
        4
    )

    if prediction == 1:

        if confidence < 0.70:

            label = "Suspicious"

        else:

            label = "Medicine"

    else:

        if confidence < 0.70:

            label = "Suspicious"

        else:

            label = "Not Medicine"

    return {
        "prediction": label,
        "confidence": confidence
    }