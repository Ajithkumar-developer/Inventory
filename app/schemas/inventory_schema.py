from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InventoryBase(BaseModel):
    ItemCode: Optional[str]
    ItemName: Optional[str]
    Category: Optional[str]
    Description: Optional[str]

    DeviceId: Optional[int]

    UnitWeight: Optional[float]
    Stock: Optional[float]
    Threshold: Optional[float]
    StockOut: Optional[float]
    Consumption: Optional[float]

    Status: Optional[str]

    class Config:
        from_attributes = True


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(InventoryBase):
    pass


class InventoryRead(InventoryBase):
    InventoryId: int
    CreatedAt: datetime
    UpdatedAt: datetime


# ---------- Special Updates ----------

class StockUpdate(BaseModel):
    Stock: float


class DeviceAssign(BaseModel):
    DeviceId: int
