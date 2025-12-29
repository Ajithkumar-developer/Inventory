from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    ItemName: str
    Category: Optional[str]
    Description: Optional[str]
    PerUnitWeight: float
    Measurement: Optional[str]
    MinThreshold: Optional[float]
    MaxThreshold: Optional[float]

    class Config:
        from_attributes = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    ItemName: Optional[str]
    Category: Optional[str]
    Description: Optional[str]
    PerUnitWeight: Optional[float]
    Measurement: Optional[str]
    MinThreshold: Optional[float]
    MaxThreshold: Optional[float]


class ItemRead(ItemBase):
    ItemId: int
    CreatedAt: datetime
    UpdatedAt: datetime
