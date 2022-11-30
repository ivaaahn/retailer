from dataclasses import asdict
from unittest.mock import AsyncMock

from app.dto.api.shop import ShopListPagingParams, ShopListRespDTO, ShopRespDTO
from app.dto.db.products import DBShopProductListDTO
from app.services.shop import ShopsService
from pytest_mock import MockerFixture
from tests.builders.db.shops import DBShopBuilder
from tests.mocks import ShopsRepoMock
from tests.mocks.repo.products import ProductsRepoMock


class TestShops:
    SHOP_ID_MOCKED = 1

    async def test_get(
        self,
        mocker: MockerFixture,
        shops_service: ShopsService,
        shops_repo_mock: ShopsRepoMock,
        orders_repo_mock: ProductsRepoMock,
        default_shop_to_build: DBShopBuilder,
    ) -> None:
        repo_shop = default_shop_to_build.build()

        shops_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=shops_repo_mock,
            attribute="get_shop",
            return_value=repo_shop,
        )

        expected = ShopRespDTO(**asdict(repo_shop))
        received = await shops_service.get(self.SHOP_ID_MOCKED)

        assert received == expected
        shops_repo_get_mocked.assert_awaited_once_with(self.SHOP_ID_MOCKED)

    async def test_get_list(
        self,
        mocker: MockerFixture,
        default_shop_paging_params: ShopListPagingParams,
        shops_service: ShopsService,
        shops_repo_mock: ShopsRepoMock,
        orders_repo_mock: ProductsRepoMock,
        default_shop_list_built: DBShopProductListDTO,
    ) -> None:
        repo_shop_list = default_shop_list_built
        paging_params = default_shop_paging_params

        shops_repo_get_list_mocked: AsyncMock = mocker.patch.object(
            target=shops_repo_mock,
            attribute="get_list",
            return_value=repo_shop_list,
        )

        expected = ShopListRespDTO(**asdict(repo_shop_list))
        received = await shops_service.get_list(paging_params)

        assert received == expected
        shops_repo_get_list_mocked.assert_awaited_once_with(paging_params)
