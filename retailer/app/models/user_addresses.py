from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("UserAddressModel",)


class UserAddressModel(BaseModel):
    __tablename__ = "user_addresses"

    id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    city = Column(Text, nullable=False, index=True)
    street = Column(Text, nullable=False, index=True)
    house = Column(Text, nullable=False)
    entrance = Column(Integer, nullable=False)
    floor = Column(Integer, nullable=True)
    flat = Column(Text, nullable=True)
