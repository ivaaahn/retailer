from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.delivery.shop.deps import shop_paging_params
from app.dto.shop import ShopListPagingParams
from app.models.shop_addresses import ShopAddressModel
from app.models.shops import ShopModel

__all__ = ("ShopsRepo",)

from app.repos.shop.interface import IShopsRepo


@lru_cache
class ShopsRepo(IShopsRepo, BasePgRepo):
    async def get_shop(self, id: int) -> Optional[ShopModel]:
        sp = ShopModel.__table__
        adr = ShopAddressModel.__table__

        stmt = select(sp.c.id, adr).where(sp.c.id == id).select_from(sp.join(adr))

        cursor = await self._execute(stmt)
        c = cursor.first()

        return ShopModel(
            id=c.id,
            address_city=c.shop_addresses_city,
            address_street=c.shop_addresses_street,
            address_house=c.shop_addresses_house,
            address_floor=c.shop_addresses_floor,
        )

    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> tuple[list[ShopModel], int]:
        sp = ShopModel.__table__
        adr = ShopAddressModel.__table__

        stmt = select(sp.c.id, adr).select_from(sp.join(adr))
        query = self.with_pagination(
            query=stmt,
            count=paging_params.count,
            offset=paging_params.offset,
            order=paging_params.order,
            sort=getattr(sp.c, paging_params.sort_by.value),
        )

        stmt_total = select(func.count()).select_from(sp.join(adr))

        cursor_count = await self._execute(stmt_total)
        total = cursor_count.scalar()
        cursor = await self._execute(query)
        return ([
            ShopModel(
                id=shop.id,
                address_city=shop.shop_addresses_city,
                address_street=shop.shop_addresses_street,
                address_house=shop.shop_addresses_house,
                address_floor=shop.shop_addresses_floor,
            )
            for shop in cursor
        ], total)
