from sqlalchemy import Column, Integer, String
from .sql_base import Base


# -------------------------------
#   ORDER MODEL
# -------------------------------
class Order(Base):
    __tablename__ = "Orders"

    OrderId = Column(Integer, primary_key=True, index=True)

    ItemCode = Column(String(100), nullable=True)
    ItemName = Column(String(255), nullable=True)
    Vendor = Column(String(255), nullable=True)

    Quantity = Column(Integer, nullable=True)
    Status = Column(String(50), nullable=True)
