import pytest
from app.base.repo import BasePgRepo, BaseRedisRepo
from app.dto.api.products import ProductListPagingParams
from app.dto.db.products import DBShopProductDTO, DBShopProductListDTO
from app.services.products.interfaces import IProductsCacheRepo, IProductsRepo
from store import PgAccessor
from store.pg.config import PgConfig
from store.redis import RedisAccessor
from store.redis.config import RedisConfig


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
