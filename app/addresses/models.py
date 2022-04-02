from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
)
from app.base.models import BaseModel


class ShopAddresses(BaseModel):
    __tablename__ = "shop_addresses"

    id = Column(Integer, Identity(), primary_key=True)
    city = Column(Text, nullable=False, index=True)
    street = Column(Text, nullable=False, index=True)
    house = Column(Text, nullable=False)
    building = Column(Text, nullable=True)
    floor = Column(Integer, nullable=True)


class CustomerAddresses(BaseModel):
    __tablename__ = "customer_addresses"

    id = Column(Integer, Identity(), primary_key=True)
    city = Column(Text, nullable=False, index=True)
    street = Column(Text, nullable=False, index=True)
    house = Column(Text, nullable=False)
    entrance = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=True)
    flat = Column(Text, nullable=True)
