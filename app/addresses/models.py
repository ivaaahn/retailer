from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
)

from app.base.models import BaseModel


class Addresses(BaseModel):
    __tablename__ = "addresses"

    id = Column(Integer, Identity(), primary_key=True)
    city = Column(Text, nullable=False)
    street = Column(Text, nullable=False)
    house = Column(Text, nullable=False)
    entrance = Column(Integer, nullable=True)
    floor = Column(Integer, nullable=True)
    flat = Column(Integer, nullable=True)
