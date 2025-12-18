from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .sql_base import Base


# -------------------------------
#   USER MODEL
# -------------------------------
class User(Base):
    __tablename__ = "User"

    UserId = Column(Integer, primary_key=True, index=True)

    Name = Column(String(255), nullable=True)
    Email = Column(String(255), nullable=False, unique=True)
    PasswordHash = Column(String(255), nullable=False)
    MobileNo = Column(String(20), nullable=True)

    CreatedAt = Column(DateTime, default=datetime.utcnow)
    UpdatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
