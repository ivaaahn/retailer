from sqlalchemy import Column, Float, ForeignKey, Identity, Integer

from app.base.models import BaseModel

__all__ = ("OrderProductsModel",)


class OrderProductsModel(BaseModel):
    __tablename__ = "order_products"

    id = Column(Integer, Identity(), primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Float, nullable=False)
    qty = Column(Integer, nullable=False)
