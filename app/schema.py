from pydantic import BaseModel
from typing import Optional

class MedicineCreate(BaseModel):
    medicine_name: str
    quantity: int
class MedicineResponse(BaseModel):
    id: int
    medicine_name: str
    quantity: int
    class Config:
        from_attributes = True

class MedicineUpdate(BaseModel):
    medicine_name: Optional[str] = None
    quantity: Optional[int] = None