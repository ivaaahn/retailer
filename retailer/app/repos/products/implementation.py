from functools import lru_cache
from typing import Optional

from sqlalchemy import func
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.models.product_categories import ProductCategoryModel
from app.models.products import ProductModel
from app.repos.products.interface import IProductsRepo

__all__ = ("ProductsRepo",)


@lru_cache
class ProductsRepo(IProductsRepo, BasePgRepo):
    async def get(self, name: str) -> Optional[ProductModel]:
        pt = ProductModel.__table__
        ct = ProductCategoryModel.__table__

        stmt = (
            select(pt, ct.c.name)
            .where(func.lower(pt.c.name) == name.lower())
            .select_from(pt.join(ct))
        )

        cursor = await self._execute(stmt)
        c = cursor.first()

        return ProductModel(
            id=c.id,
            name=c.name,
            category_name=c.product_categories_name,
            description=c.description,
        )
