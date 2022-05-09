from dataclasses import dataclass
from typing import Optional


@dataclass
class DBShopAddressDTO:
    city: Optional[str]
    street: Optional[str]
    house: Optional[str]
    floor: Optional[int]


@dataclass
class DBShopDTO:
    id: int
    address: DBShopAddressDTO


@dataclass
class DBShopListDTO:
    shops: list[DBShopDTO]
    total: int
