from app.base.models import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Identity, Integer

__all__ = ("ShopProductsModel",)


class ShopProductsModel(BaseModel):
    __tablename__ = "shop_products"

    id = Column(Integer, Identity(), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    qty = Column(Integer, nullable=False)
