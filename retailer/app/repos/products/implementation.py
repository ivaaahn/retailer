from functools import lru_cache
from typing import Optional

from sqlalchemy import func, and_
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.models.product_categories import ProductCategoryModel
from app.models.products import ProductModel
from app.models.shop_products import ShopProductsModel
from app.repos.products.interface import IProductsRepo

__all__ = ("ProductsRepo",)


@lru_cache
class ProductsRepo(IProductsRepo, BasePgRepo):
    async def get(self, product_id: int, shop_id: int) -> Optional[ProductModel]:
        pt = ProductModel.__table__
        sppt = ShopProductsModel.__table__
        ct = ProductCategoryModel.__table__

        stmt = (
            select(pt, sppt, ct)
            .where(and_(pt.c.id == product_id, sppt.c.shop_id == shop_id))
            .select_from(sppt.join(pt).join(ct))
        )

        cursor = await self._execute(stmt)
        c = cursor.first()

        return ProductModel(
            id=c.id,
            name=c.name,
            description=c.description,
            photo=c.photo,
            price=c.shop_products_price,
            category_name=c.product_categories_name
        )
