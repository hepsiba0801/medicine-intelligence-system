from sqlalchemy.orm import Session
from app.models import MedicineInventory
from app.schema import MedicineCreate, MedicineUpdate
from ml.predict import predict_medicine


# CREATE
def create_medicine(
    medicine: MedicineCreate,
    db: Session
):
    db_medicine = MedicineInventory(
        medicine_name=medicine.medicine_name,
        quantity=medicine.quantity
    )

    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return db_medicine


# READ ALL
def get_all_medicines(
    db: Session
):
    return db.query(
        MedicineInventory
    ).all()


# READ ONE
def get_medicine(
    medicine_id: int,
    db: Session
):
    return (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.id == medicine_id
        )
        .first()
    )


# UPDATE
def update_medicine(
    medicine_id: int,
    medicine_data: MedicineUpdate,
    db: Session
):
    medicine = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.id == medicine_id
        )
        .first()
    )

    if not medicine:
        return None

    update_data = medicine_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            medicine,
            field,
            value
        )

    db.commit()
    db.refresh(medicine)

    return medicine


# DELETE
def delete_medicine(
    medicine_id: int,
    db: Session
):
    medicine = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.id == medicine_id
        )
        .first()
    )

    if not medicine:
        return None

    db.delete(medicine)
    db.commit()

    return {
        "message": f"Medicine with id {medicine_id} deleted successfully"
    }


# GET ALL ANOMALIES
def get_anomalies(
    db: Session
):
    medicines = db.query(
        MedicineInventory
    ).all()

    anomalies = []

    for medicine in medicines:

        result = predict_medicine(
            medicine.medicine_name
        )

        if result["prediction"] == "Not Medicine":

            anomalies.append({
                "id": medicine.id,
                "medicine_name": medicine.medicine_name,
                "quantity": medicine.quantity,
                "prediction": result["prediction"],
                "confidence": result["confidence"]
            })

    return anomalies


# GET ANOMALY BY ID
def get_anomaly_by_id(
    medicine_id: int,
    db: Session
):
    medicine = (
        db.query(MedicineInventory)
        .filter(
            MedicineInventory.id == medicine_id
        )
        .first()
    )

    if not medicine:
        return None

    result = predict_medicine(
        medicine.medicine_name
    )

    return {
        "id": medicine.id,
        "medicine_name": medicine.medicine_name,
        "quantity": medicine.quantity,
        "prediction": result["prediction"],
        "confidence": result["confidence"]
    }


# FILTER ANOMALIES
def filter_anomalies(
    status: str,
    db: Session
):
    medicines = db.query(
        MedicineInventory
    ).all()

    results = []

    for medicine in medicines:

        result = predict_medicine(
            medicine.medicine_name
        )

        if (
            result["prediction"].lower()
            ==
            status.lower()
        ):

            results.append({
                "id": medicine.id,
                "medicine_name": medicine.medicine_name,
                "quantity": medicine.quantity,
                "prediction": result["prediction"],
                "confidence": result["confidence"]
            })

    return results