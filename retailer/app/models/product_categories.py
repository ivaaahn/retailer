from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
)

from app.base.models import BaseModel

__all__ = ("ProductCategoryModel",)


class ProductCategoryModel(BaseModel):
    __tablename__ = "product_categories"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(Text, nullable=False)
