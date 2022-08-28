from dataclasses import dataclass
from typing import Optional


@dataclass
class DBShopAddressDTO:
    city: str | None
    street: str | None
    house: str | None
    floor: int | None


@dataclass
class DBShopDTO:
    id: int
    address: DBShopAddressDTO


@dataclass
class DBShopListDTO:
    shops: list[DBShopDTO]
    total: int
