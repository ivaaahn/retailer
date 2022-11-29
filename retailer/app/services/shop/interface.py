from abc import ABC, abstractmethod

from app.dto.api.shop import ShopListPagingParams
from app.dto.db.shops import DBShopDTO, DBShopListDTO


class IShopsRepo(ABC):
    @abstractmethod
    async def get_shop(self, id: int) -> DBShopDTO | None:
        pass

    @abstractmethod
    async def get_list(
        self, paging_params: ShopListPagingParams
    ) -> DBShopListDTO:
        pass
