from dataclasses import dataclass
from enum import Enum

from app.base.deps import BasePagingParams
from pydantic import BaseModel, Field


class ShopListSortByEnum(str, Enum):
    id = "id"


@dataclass
class ShopListPagingParams(BasePagingParams):
    sort_by: ShopListSortByEnum


class ShopAddressDTO(BaseModel):
    city: str = Field(title="Город")
    street: str = Field(title="Улица")
    house: str = Field(title="Дом")
    floor: str | None = Field(title="Этаж")


class ShopRespDTO(BaseModel):
    id: int = Field(title="Идентификатор магазина")
    address: ShopAddressDTO = Field(title="Адрес магазина")


class ShopListRespDTO(BaseModel):
    shops: list[ShopRespDTO] = Field(title="Список магазинов")
    total: int = Field(title="Общее кол-во магазинов")
