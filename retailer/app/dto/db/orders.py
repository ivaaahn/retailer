from dataclasses import dataclass

from sqlalchemy import DateTime

from app.dto.db.products import DBShopProductDTO
from app.dto.db.profile import DBAddressDTO


@dataclass
class DBOrdersDTO:
    id: int
    total_price: float
    receive_kind: str
    status: str
    created_at: DateTime


@dataclass
class DBOrderProductsDTO(DBOrdersDTO):
    delivery_address: DBAddressDTO | None
    products: list[DBShopProductDTO]


@dataclass
class DBOrderProductsListDTO:
    orders: list[DBOrdersDTO]
    total: int


@dataclass
class DBPlaceOrderDTO:
    order_id: int
