from pydantic import BaseModel
from typing import Optional


class OrderBase(BaseModel):
    ItemCode: Optional[str]
    ItemName: Optional[str]
    Vendor: Optional[str]
    Quantity: Optional[int]
    Status: Optional[str]

    class Config:
        from_attributes = True


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderRead(OrderBase):
    OrderId: int
