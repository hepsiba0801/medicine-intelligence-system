from fastapi import FastAPI
from app.database import engine
from app.database import Base
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from app.schema import MedicineCreate
from app.schema import MedicineResponse
from app import crud
from fastapi import FastAPI, Depends, HTTPException
from app.schema import MedicineUpdate
from fastapi import Query
from app.schema import (
    CleaningSummary,
    CleanInventoryListResponse
)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Medicine Inventory API")

@app.get("/")
def home():
    return {"message": "Medicine Inventory API Running"}

@app.get("/medicines",response_model=list[MedicineResponse])
def get_all_medicines(db: Session = Depends(get_db)):
    return crud.get_all_medicines(db)

@app.get("/medicine/{medicine_id}",response_model=MedicineResponse)
def get_medicine(medicine_id: int,db: Session = Depends(get_db)):
    medicine = crud.get_medicine(medicine_id,db)
    if not medicine:
        raise HTTPException(status_code=404,detail=f"Medicine with id {medicine_id} not found")
    return medicine

@app.post("/medicine")
def create_medicine(medicine: MedicineCreate,db: Session = Depends(get_db)):
    return crud.create_medicine(medicine,db)

@app.put("/medicine/{medicine_id}")
def update_medicine(medicine_id: int,medicine: MedicineUpdate,db: Session = Depends(get_db)):
    updated = crud.update_medicine(medicine_id,medicine,db)
    if not updated:
        raise HTTPException(status_code=404,detail=f"Medicine with id {medicine_id} not found")
    return updated

@app.delete("/medicine/{medicine_id}")
def delete_medicine(medicine_id: int,db: Session = Depends(get_db)):
    deleted = crud.delete_medicine(medicine_id,db)
    if not deleted:
        raise HTTPException(status_code=404,detail=f"Medicine with id {medicine_id} not found")
    return deleted

@app.get("/anomalies")
def get_anomalies(db: Session = Depends(get_db)):
    return crud.get_anomalies(db)

@app.get("/anomalies/filter")
def filter_anomalies(status: str = Query(...),db: Session = Depends(get_db)):
    return crud.filter_anomalies(status,db)

@app.get("/anomalies/{medicine_id}")
def get_anomaly_by_id(medicine_id: int,db: Session = Depends(get_db)):
    result = crud.get_anomaly_by_id(medicine_id,db)
    if not result:
        raise HTTPException(status_code=404,detail=f"Medicine with id {medicine_id} not found")
    return result

@app.post("/inventory/clean")
def run_cleaning_pipeline(db: Session = Depends(get_db)):
    return crud.clean_inventory_data(db)

@app.get("/clean-inventory",response_model=CleanInventoryListResponse)
def get_clean_inventory(db: Session = Depends(get_db)):
    return crud.get_clean_inventory(db)

