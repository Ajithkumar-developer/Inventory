from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .sql_base import Base


# -------------------------------
#   INVENTORY MODEL
# -------------------------------
class Inventory(Base):
    __tablename__ = "Inventory"

    InventoryId = Column(Integer, primary_key=True, index=True)

    ItemCode = Column(String(100), nullable=True)
    ItemName = Column(String(255), nullable=True)
    Category = Column(String(100), nullable=True)
    Description = Column(String(500), nullable=True)

    DeviceId = Column(Integer, nullable=True)

    UnitWeight = Column(Float, nullable=True)
    Stock = Column(Float, nullable=True)
    Threshold = Column(Float, nullable=True)
    StockOut = Column(Float, nullable=True)
    Consumption = Column(Float, nullable=True)

    Status = Column(String(50), nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
