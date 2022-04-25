from dataclasses import dataclass
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.base.deps import BasePagingParams


class ProductListSortByEnum(str, Enum):
    id = "id"
    name = "name"


@dataclass
class ProductListPagingParams(BasePagingParams):
    sort_by: ProductListSortByEnum


class ProductRespDTO(BaseModel):
    name: str = Field(title="Название продукта")
    description: Optional[str] = Field(title="Описание продукта")
    price: float = Field(title="Цена продукта")
    category: str = Field(title="Категория продукта")
    qty: int = Field(title="Кол-во продукта")


class ProductListRespDTO(BaseModel):
    products: list[ProductRespDTO] = Field(title="Список продуктов")
    total: int = Field(title="Общее кол-во продуктов")
