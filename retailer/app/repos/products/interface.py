import abc

from app.dto.api.products import ProductListPagingParams
from app.dto.db.products import DBShopProductDTO, DBShopProductListDTO

__all__ = ("IProductsRepo", "IProductsCacheRepo")


class IProductsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        pass

    @abc.abstractmethod
    async def get_list(
        self,
        shop_id: int,
        paging_params: ProductListPagingParams,
    ) -> DBShopProductListDTO:
        pass


class IProductsCacheRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        pass

    @abc.abstractmethod
    async def save(
        self, product_id: int, shop_id: int, product_data: DBShopProductDTO
    ) -> int:
        pass
