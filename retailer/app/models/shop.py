from sqlalchemy import (
    Column,
    Integer,
    Identity,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("ShopModel",)


class ShopModel(BaseModel):
    __tablename__ = "shop"

    id = Column(Integer, Identity(), primary_key=True)
    address_id = Column(Integer, ForeignKey("shops_address.id"), nullable=False)
