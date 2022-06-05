from dataclasses import dataclass
from typing import Any, Optional

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
