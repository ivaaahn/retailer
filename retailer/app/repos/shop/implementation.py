from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.delivery.shop.deps import shop_paging_params
from app.dto.api.shop import ShopListPagingParams
from app.dto.db.shops import DBShopDTO, DBShopListDTO, DBShopAddressDTO
from app.models.shop_addresses import ShopAddressModel
from app.models.shops import ShopModel
from .interface import IShopsRepo

__all__ = ("ShopsRepo",)


@lru_cache
class ShopsRepo(IShopsRepo, BasePgRepo):
    async def get_shop(self, id: int) -> Optional[DBShopDTO]:
        sp = ShopModel.__table__
        adr = ShopAddressModel.__table__

        stmt = select(sp.c.id, adr).where(sp.c.id == id).select_from(sp.join(adr))
        shop = await self.get_one(stmt)

        return DBShopDTO(
            id=shop.id,
            address=DBShopAddressDTO(
                city=shop.shop_addresses_city,
                street=shop.shop_addresses_street,
                house=shop.shop_addresses_house,
                floor=shop.shop_addresses_floor,
            ),
        )

    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> DBShopListDTO:
        sp = ShopModel.__table__
        adr = ShopAddressModel.__table__

        query_total = select(func.count()).select_from(sp.join(adr))
        query_shops = self.with_pagination(
            query=select(sp.c.id, adr).select_from(sp.join(adr)),
            count=paging_params.count,
            offset=paging_params.offset,
            order=paging_params.order,
            sort=getattr(sp.c, paging_params.sort_by.value),
        )

        total = await self.get_scalar(query_total)
        cursor_shops = await self._execute(query_shops)
        shops = [
            DBShopDTO(
                id=shop.id,
                address=DBShopAddressDTO(
                    city=shop.shop_addresses_city,
                    street=shop.shop_addresses_street,
                    house=shop.shop_addresses_house,
                    floor=shop.shop_addresses_floor,
                ),
            )
            for shop in cursor_shops
        ]

        return DBShopListDTO(shops=shops, total=total)
