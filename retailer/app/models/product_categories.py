from app.base.models import BaseModel
from sqlalchemy import Column, Identity, Index, Integer, Text, func

__all__ = ("ProductCategoryModel",)


class ProductCategoryModel(BaseModel):
    __tablename__ = "product_categories"
    __table_args__ = (
        Index(
            "idx_products_categories_lower",
            func.lower("product_categories.name"),
            unique=True,
        ),
    )

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(Text, nullable=False)
