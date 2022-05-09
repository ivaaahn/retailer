import json
from dataclasses import asdict
from functools import lru_cache

from sqlalchemy import and_
from sqlalchemy.future import select

from app.base.repo import BasePgRepo, BaseRedisRepo
from app.delivery.products.errors import ProductNotFoundError
from app.dto.db.products import DBShopProductDTO
from app.misc import make_shop_product_key
from app.models.product_categories import ProductCategoryModel
from app.models.products import ProductModel
from app.models.shop_products import ShopProductsModel
from .interface import IProductsRepo

__all__ = ("ProductsRepo", "ProductsCacheRepo")


@lru_cache
class ProductsRepo(IProductsRepo, BasePgRepo):
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        pt = ProductModel.__table__
        spt = ShopProductsModel.__table__
        pct = ProductCategoryModel.__table__

        stmt = (
            select(pt, spt, pct)
            .where(and_(pt.c.id == product_id, spt.c.shop_id == shop_id))
            .select_from(spt.join(pt).join(pct))
        )

        product = await self.get_one(stmt)

        if not product:
            raise ProductNotFoundError(product_id, shop_id)

        return DBShopProductDTO(
            id=product_id,
            name=product.name,
            price=product.price,
            category=product.product_categories_name,
            description=product.description,
            photo=product.photo,
            qty=product.qty,
        )


class ProductsCacheRepo(BaseRedisRepo):
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        result = await self._redis.cli.get(
            name=make_shop_product_key(product_id, shop_id),
        )

        if not result:
            raise ProductNotFoundError(product_id, shop_id)

        return DBShopProductDTO(**json.loads(result))

    async def save(
        self, product_id: int, shop_id: int, product_data: DBShopProductDTO
    ) -> int:
        result = await self._redis.cli.set(
            name=make_shop_product_key(product_id, shop_id),
            value=json.dumps(asdict(product_data)),
        )

        return result
