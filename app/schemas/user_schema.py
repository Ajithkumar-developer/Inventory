from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    Name: Optional[str]
    Email: Optional[str]
    MobileNo: Optional[str]

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    Email: str
    Password: str


class UserUpdate(UserBase):
    Password: Optional[str]


class UserRead(UserBase):
    UserId: int
    CreatedAt: datetime
    UpdatedAt: datetime


class LoginRequest(BaseModel):
    Email: str
    Password: str
