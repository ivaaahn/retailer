import copy
from datetime import datetime

from retailer.app.dto.db.orders import DBOrderProductsDTO, DBOrdersDTO
from retailer.app.dto.db.products import DBShopProductDTO
from retailer.app.dto.db.profile import DBAddressDTO
from retailer.app.models.orders import OrderReceiveKindEnum, OrderStatusEnum
from retailer.tests.builders.db.common import BaseBuilder
from retailer.tests.constants import DEFAULT_DATETIME


class DBOrderBuilder(BaseBuilder):
    def __init__(self):
        self._id = 1
        self._total_price = 1000
        self._receive_kind = OrderReceiveKindEnum.takeaway
        self._status = OrderStatusEnum.collecting
        self._created_at = DEFAULT_DATETIME
        self._delivery_address = 1

    def but(self) -> "DBOrderBuilder":
        return copy.deepcopy(self)

    def with_id(self, value: int) -> "DBOrderBuilder":
        self._id = value
        return self

    def with_total_price(self, value: int) -> "DBOrderBuilder":
        self._total_price = value
        return self

    def with_receive_kind(
        self, value: OrderReceiveKindEnum
    ) -> "DBOrderBuilder":
        self._receive_kind = value
        return self

    def with_status(self, value: OrderStatusEnum) -> "DBOrderBuilder":
        self._status = value
        return self

    def with_created_at(self, value: datetime) -> "DBOrderBuilder":
        self._created_at = value
        return self

    def with_delivery_address(self, value: int) -> "DBOrderBuilder":
        self._delivery_address = value
        return self

    def build(self) -> DBOrdersDTO:
        return DBOrdersDTO(
            id=self._id,
            total_price=self._total_price,
            receive_kind=self._receive_kind,
            status=self._status,
            created_at=self._created_at,
            delivery_address=self._delivery_address,
        )


class DBOrderProductsBuilder(DBOrderBuilder):
    def __init__(self) -> None:
        super().__init__()
        self._delivery_address = DBAddressDTO(
            1, "some city", "street", "house", 1, 1, 1
        )
        self._products: list[DBShopProductDTO] = []

    def with_delivery_address(
        self, value: DBAddressDTO
    ) -> "DBOrderProductsBuilder":
        self._delivery_address = value
        return self

    def with_products(
        self, value: list[DBShopProductDTO]
    ) -> "DBOrderProductsBuilder":
        self._products = value
        return self

    def build(self) -> DBOrderProductsDTO:
        return DBOrderProductsDTO(
            id=self._id,
            total_price=self._total_price,
            receive_kind=self._receive_kind,
            status=self._status,
            created_at=self._created_at,
            delivery_address=self._delivery_address,
            products=self._products,
        )
