from dataclasses import asdict

from fastapi import Depends

from retailer.app.base.services import BaseService
from retailer.app.delivery.shop.deps import shop_paging_params
from retailer.app.delivery.shop.errors import ShopNotFoundError
from retailer.app.dto.api.shop import (
    ShopListPagingParams,
    ShopListRespDTO,
    ShopRespDTO,
)
from retailer.app.repos.shop import ShopsRepo
from retailer.app.services.shop.interface import IShopsRepo

__all__ = ("ShopsService",)


class ShopsService(BaseService):
    def __init__(self, shops_repo: IShopsRepo = Depends(ShopsRepo)):
        super().__init__()
        self._shops_repo = shops_repo

    async def get(self, id: int) -> ShopRespDTO:
        received = await self._shops_repo.get_shop(id)

        if not received:
            raise ShopNotFoundError(id)

        return ShopRespDTO(**asdict(received))

    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> ShopListRespDTO:
        shops_list = await self._shops_repo.get_list(paging_params)
        return ShopListRespDTO(**asdict(shops_list))
