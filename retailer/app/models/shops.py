from sqlalchemy import (
    Column,
    Integer,
    Identity,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("ShopModel",)


class ShopModel(BaseModel):
    __tablename__ = "shops"

    id = Column(Integer, Identity(), primary_key=True)
    address_id = Column(Integer, ForeignKey("shop_addresses.id"), nullable=False)
