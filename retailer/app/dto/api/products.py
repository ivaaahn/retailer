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


class BaseProduct(BaseModel):
    id: int = Field(title="Идентификатор продукта")
    photo: str | None = Field(title="Фото продукта")
    name: str = Field(title="Название продукта")
    description: str | None = Field(title="Описание продукта")
    price: float = Field(title="Цена продукта")
    category: str = Field(title="Категория продукта")


class ShopProductDTO(BaseProduct):
    price: float = Field(title="Цена продукта в магазине")
    availability: int = Field(title="Кол-во продуктов в наличии")


class CartProductDTO(BaseModel):
    product: ShopProductDTO = Field(title="Продукт")
    qty: int = Field(title="Кол-во продукта в корзине")
    price: float = Field(title="Суммарная цена продукта")


class ShopProductsListDTO(BaseModel):
    products: list[ShopProductDTO] = Field(title="Список продуктов")
    total: float = Field(title="Общее кол-во продуктов")
