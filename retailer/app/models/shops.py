from sqlalchemy import Column, ForeignKey, Identity, Integer

from retailer.app.base.models import BaseModel

__all__ = ("ShopModel",)


class ShopModel(BaseModel):
    __tablename__ = "shops"

    id = Column(Integer, Identity(), primary_key=True)
    address_id = Column(
        Integer, ForeignKey("shop_addresses.id"), nullable=False
    )
