import pytest

from retailer.app.base.repo import BasePgRepo, BaseRedisRepo
from retailer.app.dto.api.products import ProductListPagingParams
from retailer.app.dto.db.products import DBShopProductDTO, DBShopProductListDTO
from retailer.app.services.products.interfaces import (
    IProductsCacheRepo,
    IProductsRepo,
)
from retailer.store import PgAccessor
from retailer.store.pg.config import PgConfig
from retailer.store.redis import RedisAccessor
from retailer.store.redis.config import RedisConfig


class ProductsRepoMock(IProductsRepo, BasePgRepo):
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        pass

    async def get_list(
        self, shop_id: int, paging_params: ProductListPagingParams
    ) -> DBShopProductListDTO:
        pass


class ProductsCacheRepoMock(IProductsCacheRepo, BaseRedisRepo):
    async def get(self, product_id: int, shop_id: int) -> DBShopProductDTO:
        pass

    async def save(
        self, product_id: int, shop_id: int, product_data: DBShopProductDTO
    ) -> int:
        pass


@pytest.fixture
def products_repo_mock() -> ProductsRepoMock:
    return ProductsRepoMock(PgAccessor(PgConfig()))


@pytest.fixture
def products_cache_repo_mock() -> ProductsCacheRepoMock:
    return ProductsCacheRepoMock(RedisAccessor(RedisConfig()))
