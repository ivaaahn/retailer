from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    Identity,
    ForeignKey,
)

from app.base.models import BaseModel

__all__ = ("ShopModel",)


class ShopModel(BaseModel):
    __tablename__ = "shops"

    id = Column(Integer, Identity(), primary_key=True)
    address_id = Column(Integer, ForeignKey("shop_addresses.id"), nullable=False)

    def __init__(
        self,
        address_city: Optional[str] = None,
        address_street: Optional[str] = None,
        address_house: Optional[str] = None,
        address_floor: Optional[int] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._address_city = address_city
        self._address_street = address_street
        self._address_house = address_house
        self._address_floor = address_floor

    def _as_dict(self) -> dict:
        return {
            "id": self.id,
            "city": self.adr_city,
            "street": self.adr_street,
            "house": self.adr_house,
            "floor": self.adr_floor,
        }

    @property
    def adr_city(self) -> str:
        return self._address_city

    @adr_city.setter
    def adr_city(self, value: str):
        self._address_city = value

    @property
    def adr_street(self) -> str:
        return self._address_street

    @adr_street.setter
    def adr_street(self, value: str):
        self._address_street = value

    @property
    def adr_house(self) -> str:
        return self._address_house

    @adr_house.setter
    def adr_house(self, value: str):
        self._address_house = value

    @property
    def adr_floor(self) -> int:
        return self._address_floor

    @adr_floor.setter
    def adr_floor(self, value: int):
        self._address_floor = value
