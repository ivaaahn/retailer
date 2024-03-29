from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DBProductBaseDTO:
    id: int
    name: str
    photo: str
    description: str
    category: str | None


@dataclass
class DBShopProductDTO(DBProductBaseDTO):
    price: float
    availability: int

    @classmethod
    def from_db(cls, db: Any | None) -> Optional["DBShopProductDTO"]:
        if not db:
            return None

        return cls(
            id=db.id,
            photo=db.photo,
            name=db.name,
            description=db.description,
            price=db.price,
            category=db.product_categories_name,
            availability=db.order_products_qty,
        )


@dataclass
class DBCartProductDTO:
    product_id: int
    qty: int


@dataclass
class DBCartInfoDTO:
    products: list[DBCartProductDTO]


@dataclass
class DBShopProductListDTO:
    products: list[DBShopProductDTO]
    total: int
