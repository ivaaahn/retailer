from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ProductListSortByEnum(str, Enum):
    id = "id"
    name = "name"


class ProductRespDTO(BaseModel):
    name: str = Field(title="Название продукта")
    description: Optional[str] = Field(title="Описание продукта")
    category: str = Field(title="Категория продукта")
    withAvailability: bool = Field(title="Наличие в магазине")


class ProductListRespDTO(BaseModel):
    products: list[ProductRespDTO] = Field(title="Список продуктов")
    total: int = Field(title="Общее кол-во продуктов")
