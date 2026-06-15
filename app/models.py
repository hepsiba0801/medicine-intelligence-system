from sqlalchemy import Column, Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from app.database import Base


class MedicineInventory(Base):
    __tablename__ = "medicine_inventory"
    id = Column(Integer,primary_key=True,autoincrement=True)
    medicine_name = Column(String(255),nullable=False,index=True)
    quantity = Column(Integer,nullable=False)

class CleanInventory(Base):
    __tablename__ = "clean_inventory"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, nullable=False, index=True)
    medicine_name = Column(String(255), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    ml_label = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)