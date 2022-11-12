import copy

from app.dto.db.profile import DBAddressDTO
from tests.builders.db.common import BaseBuilder


class AddressBuilder(BaseBuilder):
    def __init__(self):
        self._id = 1
        self._user_id = 1
        self._city = "some city"
        self._street = "some street"
        self._house = "some house"
        self._entrance = 1
        self._floor = 1
        self._flat = "1"

    def but(self) -> "AddressBuilder":
        return copy.deepcopy(self)

    def with_id(self, value: int) -> "AddressBuilder":
        self._user_id = value
        return self

    def with_city(self, value: str) -> "AddressBuilder":
        self._city = value
        return self

    def with_street(self, value: str) -> "AddressBuilder":
        self._street = value
        return self

    def with_house(self, value: str) -> "AddressBuilder":
        self._house = value
        return self

    def with_entrance(self, value: int) -> "AddressBuilder":
        self._entrance = value
        return self

    def with_floor(self, value: int) -> "AddressBuilder":
        self._floor = value
        return self

    def with_flat(self, value: int) -> "AddressBuilder":
        self._flat = value
        return self

    def build(self) -> DBAddressDTO:
        return DBAddressDTO(
            id=self._id,
            city=self._city,
            street=self._street,
            house=self._house,
            entrance=self._entrance,
            floor=self._floor,
            flat=self._flat,
        )
