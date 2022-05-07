from dataclasses import asdict
from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.delivery.shop.deps import shop_paging_params
from app.delivery.shop.errors import ShopNotFoundError
from app.dto.api.shop import (
    ShopRespDTO,
    ShopAddressDTO,
    ShopListRespDTO,
    ShopListPagingParams,
)
from app.repos.shop.implementation import ShopsRepo
from app.repos.shop.interface import IShopsRepo

__all__ = ("ShopsService",)


@lru_cache
class ShopsService(BaseService):
    def __init__(
        self,
        shops_repo: IShopsRepo = Depends(ShopsRepo),
    ):
        super().__init__()
        self._shops_repo = shops_repo

    async def get_shop(self, id: int) -> ShopRespDTO:
        received = await self._shops_repo.get_shop(id)

        if not received:
            raise ShopNotFoundError(id)

        return ShopRespDTO(**asdict(received))

    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> ShopListRespDTO:
        shops_list = await self._shops_repo.get_list(paging_params)
        return ShopListRespDTO(**asdict(shops_list))
