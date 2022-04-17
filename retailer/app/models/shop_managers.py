from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("ShopManagerModel",)


class ShopManagerModel(BaseModel):
    __tablename__ = "shop_managers"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), primary_key=True)
