from dataclasses import asdict, dataclass
from typing import Any, Optional

from retailer.app.misc import parse_product_key


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
    shop_id: int
    product_id: int

    @classmethod
    def from_db(cls, db: Any | None) -> Optional["DBShopProductDTO"]:
        if not db:
            return None

        return cls(
            id=db.id,
            shop_id=db.shop_id,
            product_id=db.product_id,
            photo=db.photo,
            name=db.name,
            description=db.description,
            price=db.price,
            category=db.product_categories_name,
            availability=db.order_products_qty,
        )

    def to_dict(self) -> dict:
        pre_dict = asdict(self)
        pre_dict.pop("product_id")
        pre_dict.pop("shop_id")
        return pre_dict


@dataclass
class DBCartProductDTO:
    product_id: int
    qty: int


@dataclass
class DBCartInfoDTO:
    products: list[DBCartProductDTO]

    @classmethod
    def from_redis(cls, products: dict) -> "DBCartInfoDTO":
        return cls(
            [
                DBCartProductDTO(
                    product_id=parse_product_key(p_key),
                    qty=int(p_value),
                )
                for p_key, p_value in products.items()
            ]
        )


@dataclass
class DBShopProductListDTO:
    products: list[DBShopProductDTO]
    total: int
