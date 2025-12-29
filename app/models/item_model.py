from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .sql_base import Base


class Item(Base):
    __tablename__ = "Item"

    ItemId = Column(Integer, primary_key=True, index=True)

    ItemName = Column(String(255), nullable=False)
    Category = Column(String(255), nullable=True)
    Description = Column(String(500), nullable=True)

    PerUnitWeight = Column(Float, nullable=False)
    Measurement = Column(String(50), nullable=True)

    MinThreshold = Column(Float, nullable=True)
    MaxThreshold = Column(Float, nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
