import abc
from typing import Optional

from fastapi import Depends

from app.delivery.shop.deps import shop_paging_params
from app.dto.shop import ShopListPagingParams
from app.models.shops import ShopModel

__all__ = ("IShopsRepo",)


class IShopsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_shop(self, id: int) -> Optional[ShopModel]:
        pass

    @abc.abstractmethod
    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> tuple[list[ShopModel], int]:
        pass
