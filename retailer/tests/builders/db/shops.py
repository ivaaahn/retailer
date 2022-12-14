import copy
from dataclasses import asdict

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from retailer.app.dto.db.shops import DBShopAddressDTO, DBShopDTO
from retailer.app.models.shop_addresses import ShopAddressModel
from retailer.app.models.shops import ShopModel
from retailer.tests.builders.db.common import BaseBuilder


async def save_shop(conn: AsyncConnection, shop: DBShopDTO) -> DBShopDTO:
    address_map = asdict(shop.address)
    address_stmt = insert(ShopAddressModel).values(**address_map)
    address_cursor = await conn.execute(address_stmt)

    shop_stmt = insert(ShopModel).values(
        {"address_id": address_cursor.inserted_primary_key[0]}
    )
    shop_cursor = await conn.execute(shop_stmt)

    shop.id = shop_cursor.inserted_primary_key[0]
    return shop


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
