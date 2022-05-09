import abc
from typing import Optional

from fastapi import Depends

from app.delivery.shop.deps import shop_paging_params
from app.dto.api.shop import ShopListPagingParams
from app.dto.db.shops import DBShopDTO, DBShopListDTO

__all__ = ("IShopsRepo",)


class IShopsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_shop(self, id: int) -> Optional[DBShopDTO]:
        pass

    @abc.abstractmethod
    async def get_list(
        self, paging_params: ShopListPagingParams = Depends(shop_paging_params)
    ) -> DBShopListDTO:
        pass
