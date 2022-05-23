from dataclasses import dataclass
from typing import Optional


@dataclass
class DBAddressDTO:
    id: int
    city: str
    street: str
    house: str
    entrance: int
    floor: Optional[int]
    flat: Optional[str]


@dataclass
class DBAddressListDTO:
    addresses: list[DBAddressDTO]
