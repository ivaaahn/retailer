from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ShopListSortByEnum(str, Enum):
    id = "id"
    address = "address"


class ShopAddressDTO(BaseModel):
    id: int = Field(title="Идентификатор адреса")
    city: str = Field(title="Город")
    street: str = Field(title="Улица")
    house: str = Field(title="Дом")
    floor: Optional[str] = Field(title="Этаж")


class ShopRespDTO(BaseModel):
    id: int = Field(title="Идентификатор магазина")
    address: ShopAddressDTO = Field(title="Адрес магазина")


class ShopListRespDTO(BaseModel):
    shops: list[ShopRespDTO] = Field(title="Список магазинов")
    total: int = Field(title="Общее кол-во магазинов")
