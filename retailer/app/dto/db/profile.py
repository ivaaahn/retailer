from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Optional


@dataclass
class DBAddressDTO:
    id: int
    city: str
    street: str
    house: str
    entrance: int
    floor: int | None
    flat: str | None

    @classmethod
    def from_db(cls, db: Mapping | None) -> Optional["DBAddressDTO"]:
        if not db:
            return None

        return cls(
            id=db["id"],
            city=db["city"],
            street=db["street"],
            house=db["house"],
            entrance=db["entrance"],
            floor=db["floor"],
            flat=db["flat"],
        )


@dataclass
class DBAddressListDTO:
    addresses: list[DBAddressDTO]

    @classmethod
    def from_db(cls, db: Iterable[Mapping]) -> "DBAddressListDTO":
        return DBAddressListDTO([DBAddressDTO.from_db(item) for item in db])
