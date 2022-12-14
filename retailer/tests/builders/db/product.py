import copy
from dataclasses import asdict
from typing import NamedTuple

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from retailer.app.dto.db.products import DBShopProductDTO
from retailer.app.dto.db.shops import DBShopDTO
from retailer.app.models.product_categories import ProductCategoryModel
from retailer.app.models.products import ProductModel
from retailer.app.models.shop_products import ShopProductsModel
from retailer.tests.builders.db.common import BaseBuilder
from retailer.tests.builders.db.shops import save_shop


async def save_product(
    conn: AsyncConnection, shop_product: DBShopProductDTO, category_id: int
) -> DBShopProductDTO:
    product_stmt = insert(ProductModel).values(
        name=shop_product.name,
        photo=shop_product.photo,
        description=shop_product.description,
        category_id=category_id,
    )
    product_cursor = await conn.execute(product_stmt)
    shop_product.product_id = product_cursor.inserted_primary_key[0]
    return shop_product


async def save_product_category(
    conn: AsyncConnection,
    shop_product: DBShopProductDTO,
) -> int:
    category_stmt = insert(ProductCategoryModel).values(
        name=shop_product.category
    )
    category_cursor = await conn.execute(category_stmt)
    return category_cursor.inserted_primary_key[0]


class SavedShopProductResponse(NamedTuple):
    shop: DBShopDTO
    shop_product: DBShopProductDTO


async def save_shop_product(
    conn: AsyncConnection, shop_product: DBShopProductDTO, shop: DBShopDTO
) -> SavedShopProductResponse:
    category_id = await save_product_category(conn, shop_product)

    shop_product = await save_product(conn, shop_product, category_id)
    shop = await save_shop(conn, shop)

    stmt = insert(ShopProductsModel).values(
        shop_id=shop.id,
        product_id=shop_product.product_id,
        price=shop_product.price,
        qty=shop_product.availability,
    )
    cursor = await conn.execute(stmt)

    shop_product.id = cursor.inserted_primary_key[0]
    return SavedShopProductResponse(
        shop=shop,
        shop_product=shop_product,
    )


class DBShopProductBuilder(BaseBuilder):
    def __init__(self):
        self._id = 1
        self._shop_id = 1
        self._product_id = 1
        self._name = "product name"
        self._photo = "https://fixme.com/fixme"
        self._description = "product description"
        self._category = "product category"
        self._price = 1000
        self._availability = 1000

    def but(self) -> "DBShopProductBuilder":
        return copy.deepcopy(self)

    def with_id(self, value: int) -> "DBShopProductBuilder":
        self._id = value
        return self

    def with_name(self, value: str) -> "DBShopProductBuilder":
        self._name = value
        return self

    def with_photo(self, value: str | None) -> "DBShopProductBuilder":
        self._photo = value
        return self

    def with_description(self, value: str) -> "DBShopProductBuilder":
        self._description = value
        return self

    def with_category(self, value: str) -> "DBShopProductBuilder":
        self._category = value
        return self

    def with_price(self, value: float) -> "DBShopProductBuilder":
        self._price = value
        return self

    def with_availability(self, value: int) -> "DBShopProductBuilder":
        self._availability = value
        return self

    def build(self) -> DBShopProductDTO:
        return DBShopProductDTO(
            id=self._id,
            shop_id=self._shop_id,
            product_id=self._product_id,
            name=self._name,
            photo=self._photo,
            description=self._description,
            category=self._category,
            price=self._price,
            availability=self._availability,
        )
