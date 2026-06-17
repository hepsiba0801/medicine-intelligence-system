from sqlalchemy.orm import Session

from app.models import (
    MedicineInventory,
    CleanInventory
)

from app.schema import (
    MedicineCreate,
    MedicineUpdate,
    CleaningSummary
)
from llm.classifier import classify_item

# CREATE
def create_medicine(medicine: MedicineCreate, db: Session):

    db_medicine = MedicineInventory(
    medicine_name=medicine.medicine_name,
    quantity=medicine.quantity
)
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return db_medicine


# READ ALL
def get_all_medicines(db: Session):
    return db.query(MedicineInventory).all()


# READ ONE
def get_medicine(medicine_id: int,db: Session):
    return (db.query(MedicineInventory).filter(MedicineInventory.id == medicine_id).first())


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
        "message": "Deleted successfully"
    }

def clean_inventory_data(db: Session):
    db.query(CleanInventory).delete()
    db.commit()
    medicines = db.query(MedicineInventory).all()
    copied = 0
    ignored = 0
    for medicine in medicines:

        result = classify_item(medicine.medicine_name)
        if not result["is_medicine"]:
            ignored += 1
            continue

        clean_row = CleanInventory(
            source_id=medicine.id,
            medicine_name=medicine.medicine_name,
            suggested_name=result["suggested_name"],
            stock_quantity=medicine.quantity,
            classification=result["category"],
            classification_confidence=result["confidence"],
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
    records = (db.query(CleanInventory).all())
    return {
        "total": len(records),
        "records": records
    }