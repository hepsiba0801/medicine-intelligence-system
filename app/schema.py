from pydantic import BaseModel, ConfigDict
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

class CleanInventoryItem(BaseModel):
    id: int
    source_id: int
    medicine_name: str
    stock_quantity: int
    ml_label: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)


class CleanInventoryListResponse(BaseModel):
    total: int
    records: list[CleanInventoryItem]


class CleaningSummary(BaseModel):
    total_processed: int
    copied: int
    ignored: int