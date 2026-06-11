from sqlalchemy import Column
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
