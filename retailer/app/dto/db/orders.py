from dataclasses import dataclass

from sqlalchemy import DateTime

from app.dto.db.products import DBShopProductDTO


@dataclass
class DBOrdersDTO:
    id: int
    total_price: float
    receive_kind: str
    status: str
    created_at: DateTime


@dataclass
class DBOrderProductsDTO(DBOrdersDTO):
    products: list[DBShopProductDTO]


@dataclass
class DBOrderProductsListDTO:
    orders: list[DBOrderProductsDTO]
    total: int


@dataclass
class DBPlaceOrderDTO:
    order_id: int
