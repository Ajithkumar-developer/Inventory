from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .sql_base import Base


# -------------------------------
#   DEVICE MODEL
# -------------------------------
class Device(Base):
    __tablename__ = "Device"

    DeviceId = Column(Integer, primary_key=True, index=True)

    DeviceName = Column(String(255), nullable=True)
    DeviceType = Column(String(100), nullable=True)
    ConnectionMode = Column(String(100), nullable=True)

    Capacity = Column(Float, nullable=True)
    # Weight = Column(Float, nullable=True)

    # LastReading = Column(Float, nullable=True)
    Battery = Column(Integer, nullable=True)
    Status = Column(String(50), nullable=True)

    # InventoryId = Column(Integer, nullable=True)

    Notes = Column(String(500), nullable=True)

    LocationName = Column(String(255), nullable=True)
    Latitude = Column(Float, nullable=True)
    Longitude = Column(Float, nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




