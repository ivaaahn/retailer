from dataclasses import dataclass
from typing import Any, Optional

from app.dto.db.products import DBShopProductDTO
from app.dto.db.profile import DBAddressDTO
from sqlalchemy import DateTime


@dataclass
class DBOrdersDTO:
    id: int
    total_price: float
    receive_kind: str
    status: str
    created_at: DateTime
    delivery_address: int

    @classmethod
    def from_db(cls, db: Any | None) -> Optional["DBOrdersDTO"]:
        if not db:
            return None

        return cls(
            id=db.id,
            total_price=db.total_price,
            receive_kind=db.receive_kind,
            status=db.status,
            created_at=db.created_at,
            delivery_address=db.address_id,
        )


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
