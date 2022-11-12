from datetime import date

from pydantic import BaseModel, Field


class ProfileUpdateReqDTO(BaseModel):
    name: str | None
    birthday: date | None = None


class AddressDTO(BaseModel):
    city: str = Field(title="Город")
    street: str = Field(title="Улица")
    house: str = Field(title="Дом")
    entrance: int = Field(title="Подъезд")
    floor: int | None = Field(title="Этаж")
    flat: str | None = Field(title="Квартира")


class AddressAddDTO(AddressDTO):
    pass


class AddressRespDTO(AddressDTO):
    id: int = Field(title="Идентификатор адреса")


class UserAddressListDTO(BaseModel):
    addresses: list[AddressRespDTO]
