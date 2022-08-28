from dataclasses import dataclass
from typing import Any, Optional


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
    def from_db(cls, db: Any | None) -> Optional["DBAddressDTO"]:
        return (
            cls(
                id=db.id,
                city=db.city,
                street=db.street,
                house=db.house,
                entrance=db.entrance,
                floor=db.floor,
                flat=db.flat,
            )
            if db
            else None
        )


@dataclass
class DBAddressListDTO:
    addresses: list[DBAddressDTO]
