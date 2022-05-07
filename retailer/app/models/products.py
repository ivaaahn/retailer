from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("ProductModel",)


class ProductModel(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(Text, nullable=False)
    photo = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)
