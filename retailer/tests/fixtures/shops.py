import pytest
from app.base.deps import SortOrderEnum
from app.dto.api.products import ProductListSortByEnum
from app.dto.api.shop import ShopListPagingParams, ShopListSortByEnum
from app.dto.db.shops import DBShopListDTO
from app.services.shop import ShopsService
from tests.builders.db.shops import DBShopBuilder
from tests.mocks import ShopsRepoMock


@pytest.fixture
def shops_service(shops_repo_mock: ShopsRepoMock) -> ShopsService:
    return ShopsService(shops_repo_mock)


@pytest.fixture
def default_shop_to_build() -> DBShopBuilder:
    return DBShopBuilder()


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
