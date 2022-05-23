from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ProfileUpdateReqDTO(BaseModel):
    name: Optional[str]
    birthday: Optional[date]


class AddressAddReqDTO(BaseModel):
    city: str = Field(title="Город")
    street: str = Field(title="Улица")
    house: str = Field(title="Дом")
    entrance: int = Field(title="Подъезд")
    floor: Optional[int] = Field(title="Этаж")
    flat: Optional[str] = Field(title="Квартира")
