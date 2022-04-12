from functools import lru_cache
from typing import Optional

from sqlalchemy import func
from sqlalchemy.exc import NoSuchColumnError
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.models.product_categories import ProductCategories
from app.models.products import Products
from app.repos.products.interface import IProductsRepo

__all__ = ("ProductsRepo",)


@lru_cache
class ProductsRepo(IProductsRepo, BasePgRepo):
    async def get(self, name: str) -> Optional[Products]:
        pt = Products.__table__
        ct = ProductCategories.__table__

        stmt = (
            select(pt.c.name, ct.c.name)
            .where(func.lower(pt.c.name) == name.lower())
            .select_from(pt.join(ct))
        )

        cursor = await self._execute(stmt)

        c = cursor.first()

        try:
            description = c["description"]
        except NoSuchColumnError:
            description = None

        return Products(
            name=c.name,
            category_name=c.product_categories_name,
            description=description,
        )
