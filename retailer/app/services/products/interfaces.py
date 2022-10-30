from abc import ABC, abstractmethod

from app.dto.api.products import ProductListPagingParams
from app.dto.db.products import DBShopProductDTO, DBShopProductListDTO


class IProductsRepo(ABC):
    @abstractmethod
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_list(
        self,
        shop_id: int,
        paging_params: ProductListPagingParams,
    ) -> DBShopProductListDTO:
        raise NotImplementedError


class IProductsCacheRepo(ABC):
    @abstractmethod
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        raise NotImplementedError

    @abstractmethod
    async def save(
        self, product_id: int, shop_id: int, product_data: DBShopProductDTO
    ) -> int:
        raise NotImplementedError
