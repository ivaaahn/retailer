from dataclasses import dataclass
from typing import Optional


@dataclass
class DBProductBaseDTO:
    id: int
    name: str
    photo: str
    description: str
    category: Optional[str]


@dataclass
class DBShopProductDTO(DBProductBaseDTO):
    price: float
    qty: int


@dataclass
class DBCartProductDTO:
    product_id: int
    qty: int


@dataclass
class DBCartProductExtDTO(DBShopProductDTO):
    product: DBShopProductDTO
    qty: int
    price: float


@dataclass
class DBCartInfoDTO:
    products: list[DBCartProductDTO]


@dataclass
class DBCartInfoExtDTO:
    products: list[DBCartProductExtDTO]
