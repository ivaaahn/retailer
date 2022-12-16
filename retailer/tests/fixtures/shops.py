import pytest

from retailer.app.base.deps import SortOrderEnum
from retailer.app.dto.api.shop import ShopListPagingParams, ShopListSortByEnum
from retailer.app.dto.db.shops import DBShopDTO, DBShopListDTO
from retailer.app.services.shop import ShopsService
from retailer.tests.builders.db.shops import DBShopBuilder
from retailer.tests.mocks import ShopsRepoMock


@pytest.fixture
def shops_service(shops_repo_mock: ShopsRepoMock) -> ShopsService:
    return ShopsService(shops_repo_mock)


@pytest.fixture
def default_shop_to_build() -> DBShopBuilder:
    return DBShopBuilder()


@pytest.fixture
def default_shop() -> DBShopDTO:
    return DBShopBuilder().build()


@pytest.fixture
def default_shop_list_built(
    default_shop_to_build: DBShopBuilder,
) -> DBShopListDTO:
    QTY = 2
    shops = [
        default_shop_to_build.but().with_id(idx).build()
        for idx in range(1, QTY + 1)
    ]

    return DBShopListDTO(
        total=QTY,
        shops=shops,
    )


@pytest.fixture
def default_shop_paging_params() -> ShopListPagingParams:
    return ShopListPagingParams(
        count=100,
        offset=0,
        order=SortOrderEnum.asc,
        sort_by=ShopListSortByEnum.id,
    )
