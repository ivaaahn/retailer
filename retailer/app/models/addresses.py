from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    ForeignKey,
)
from app.base.models import BaseModel


class CustomerAddresses(BaseModel):
    __tablename__ = "customer_addresses"

    id = Column(Integer, Identity(), primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    city = Column(Text, nullable=False, index=True)
    street = Column(Text, nullable=False, index=True)
    house = Column(Text, nullable=False)
    entrance = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=True)
    flat = Column(Text, nullable=True)
