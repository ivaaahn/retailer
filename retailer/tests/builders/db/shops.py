import copy

from app.dto.db.shops import DBShopAddressDTO, DBShopDTO
from tests.builders.db.common import BaseBuilder


class DBShopBuilder(BaseBuilder):
    def __init__(self):
        self._id = 1
        self._city = "some city"
        self._street = "some street"
        self._house = "some house"
        self._floor = 1

    def but(self) -> "DBShopBuilder":
        return copy.deepcopy(self)

    def with_id(self, value: int) -> "DBShopBuilder":
        self._id = value
        return self

    def with_city(self, value: str) -> "DBShopBuilder":
        self._city = value
        return self

    def with_street(self, value: str) -> "DBShopBuilder":
        self._street = value
        return self

    def with_house(self, value: str) -> "DBShopBuilder":
        self._house = value
        return self

    def with_floor(self, value: int) -> "DBShopBuilder":
        self._floor = value
        return self

    def build(self) -> DBShopDTO:
        return DBShopDTO(
            id=self._id,
            address=DBShopAddressDTO(
                city=self._city,
                street=self._street,
                house=self._house,
                floor=self._floor,
            ),
        )
