from ml.predict import predict_medicine
def detect_anomaly(medicine_name: str):
    prediction = predict_medicine(medicine_name)
    return prediction == "Not Medicine"