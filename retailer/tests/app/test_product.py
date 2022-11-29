from dataclasses import asdict
from unittest.mock import AsyncMock, MagicMock, call

from app.dto.api.products import (
    ProductListPagingParams,
    ShopProductDTO,
    ShopProductsListDTO,
)
from app.dto.db.products import DBShopProductListDTO
from app.services import ProductsService
from pytest_mock import MockerFixture
from tests.builders.db.product import DBProductBuilder
from tests.mocks.repo.products import ProductsRepoMock


class TestProduct:
    TEST_SHOP_ID = 1

    async def test_get(
        self,
        mocker: MockerFixture,
        make_s3_url_mocked: MagicMock,
        products_repo_mock: ProductsRepoMock,
        default_product_to_build: DBProductBuilder,
        default_product_s3_patched_to_build: DBProductBuilder,
        products_service: ProductsService,
    ) -> None:
        repo_product = default_product_to_build.build()
        product_s3_patched = default_product_s3_patched_to_build.build()

        products_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=products_repo_mock,
            attribute="get",
            return_value=repo_product,
        )
        expected = ShopProductDTO(**asdict(product_s3_patched))
        received = await products_service.get(
            product_id=repo_product.id,
            shop_id=self.TEST_SHOP_ID,
            use_cache=False,
        )

        assert received == expected
        make_s3_url_mocked.assert_called_once_with(repo_product.photo)
        products_repo_get_mocked.assert_awaited_once_with(
            repo_product.id, self.TEST_SHOP_ID
        )

    async def test_get_list(
        self,
        mocker: MockerFixture,
        make_s3_url_mocked: MagicMock,
        products_repo_mock: ProductsRepoMock,
        default_products_list_built: DBShopProductListDTO,
        default_products_list_s3_patched_built: ShopProductsListDTO,
        default_paging_params: ProductListPagingParams,
        products_service: ProductsService,
    ) -> None:
        repo_products_list = default_products_list_built

        products_repo_get_list_mocked: AsyncMock = mocker.patch.object(
            target=products_repo_mock,
            attribute="get_list",
            return_value=repo_products_list,
        )
        expected = default_products_list_s3_patched_built
        received = await products_service.get_list(
            self.TEST_SHOP_ID, default_paging_params
        )

        assert received == expected
        products_repo_get_list_mocked.assert_awaited_once_with(
            self.TEST_SHOP_ID, default_paging_params
        )
        make_s3_url_mocked.assert_has_calls(
            [call(p.photo) for p in repo_products_list.products]
        )
