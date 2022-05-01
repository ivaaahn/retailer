from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    ForeignKey,
    func,
    Index,
)

from app.base.models import BaseModel

__all__ = ("ProductModel",)


class ProductModel(BaseModel):
    __tablename__ = "products"
    __table_args__ = (
        Index(
            "idx_products_name_lower",
            func.lower("products.name"),
            unique=True,
        ),
    )

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(Text, nullable=False)
    photo = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False)

    def __init__(self, category_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._category_name = category_name

    def _as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "photo": self.photo,
            "description": self.description,
            "category_name": self.category_name,
        }

    @property
    def category_name(self) -> str:
        return self._category_name

    @category_name.setter
    def category_name(self, value: str):
        self._category_name = value
