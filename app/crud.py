from sqlalchemy.orm import Session
from app.models import MedicineInventory
from app.schema import MedicineCreate, MedicineUpdate
from ml.predict import predict_medicine
from app.models import CleanInventory
from app.schema import CleaningSummary
from ml.predict import predict_medicine

# CREATE
def create_medicine(medicine: MedicineCreate,db: Session):
    db_medicine = MedicineInventory(medicine_name=medicine.medicine_name,quantity=medicine.quantity)
    result = predict_medicine(medicine.medicine_name)

    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    response = {
        "message": "Medicine added successfully",
        "id": db_medicine.id,
        "medicine_name": db_medicine.medicine_name,
        "quantity": db_medicine.quantity,
        "prediction": result["prediction"],
        "confidence": result["confidence"]
     }
    if result["prediction"] == "Suspicious":
        response["warning"] = ("Please review this entry")
    elif result["prediction"] == "Not Medicine":
        response["warning"] = ("This item may not be a medicine")
    return response


# READ ALL
def get_all_medicines(db: Session):
    return db.query(MedicineInventory).all()


# READ ONE
def get_medicine(medicine_id: int,db: Session):
    return (db.query(MedicineInventory).filter(MedicineInventory.id == medicine_id).first())


# UPDATE
def update_medicine(medicine_id: int,medicine_data: MedicineUpdate,db: Session):
    medicine = (db.query(MedicineInventory).filter(MedicineInventory.id == medicine_id).first())

    if not medicine:
        return None
    update_data = medicine_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(medicine,field,value)
    db.commit()
    db.refresh(medicine)
    return medicine


# DELETE
def delete_medicine(medicine_id: int,db: Session):
    medicine = (db.query(MedicineInventory).filter(MedicineInventory.id == medicine_id).first())
    if not medicine:
        return None
    db.delete(medicine)
    db.commit()
    return {
        "message": f"Medicine with id {medicine_id} deleted successfully"
    }


# GET ALL ANOMALIES
def get_anomalies(db: Session):
    medicines = db.query(MedicineInventory).all()
    anomalies = []
    for medicine in medicines:
        result = predict_medicine(medicine.medicine_name)
        if result["prediction"] in ["Suspicious", "Not Medicine"]:
            anomalies.append({
                "id": medicine.id,
                "medicine_name": medicine.medicine_name,
                "quantity": medicine.quantity,
                "prediction": result["prediction"],
                "confidence": result["confidence"]
            })

    return anomalies


# GET ANOMALY BY ID
def get_anomaly_by_id(medicine_id: int,db: Session):
    medicine = (db.query(MedicineInventory).filter(MedicineInventory.id == medicine_id).first())

    if not medicine:
        return None
    result = predict_medicine(medicine.medicine_name)
    return {
        "id": medicine.id,
        "medicine_name": medicine.medicine_name,
        "quantity": medicine.quantity,
        "prediction": result["prediction"],
        "confidence": result["confidence"]
    }


# FILTER ANOMALIES
def filter_anomalies(status: str,db: Session):
    medicines = db.query(MedicineInventory).all()
    results = []

    for medicine in medicines:
        result = predict_medicine(medicine.medicine_name)
        if (result["prediction"].lower()==status.lower()):
            results.append({
                "id": medicine.id,
                "medicine_name": medicine.medicine_name,
                "quantity": medicine.quantity,
                "prediction": result["prediction"],
                "confidence": result["confidence"]
            })

    return results
def clean_inventory_data(db: Session):

    db.query(CleanInventory).delete()
    db.commit()

    medicines = db.query(MedicineInventory).all()

    copied = 0
    ignored = 0

    for medicine in medicines:

        result = predict_medicine(
            medicine.medicine_name
        )

        if result["prediction"] == "Not Medicine":
            ignored += 1
            continue

        clean_row = CleanInventory(
            source_id=medicine.id,
            medicine_name=medicine.medicine_name,
            stock_quantity=medicine.quantity,
            ml_label=result["prediction"],
            confidence=result["confidence"]
        )

        db.add(clean_row)
        copied += 1

    db.commit()

    return {
        "total_processed": len(medicines),
        "copied": copied,
        "ignored": ignored
    }


def get_clean_inventory(db: Session):

    records = db.query(CleanInventory).all()

    return {
        "total": len(records),
        "records": records
    }