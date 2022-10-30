from unittest.mock import AsyncMock, MagicMock, call

import pytest
from pytest_mock import MockerFixture

from app.dto.api.cart import CartRespDTO
from app.dto.api.products import ShopProductsListDTO
from app.dto.db.products import DBCartInfoDTO
from app.dto.db.user import DBUserDTO
from app.services import ProductsService
from app.services.carts import CartService
from tests.builders.db.product import DBProductBuilder
from tests.builders.db.user import DBUserBuilder
from tests.mocks import ProductsCacheRepoMock, ProductsRepoMock
from tests.mocks.repo.carts import CartsRepoMock


class TestCart:
    TEST_SHOP_ID = 1

    @pytest.mark.usefixtures("make_s3_url_mocked")
    async def test_get_classic_school(
        self,
        mocker: MockerFixture,
        products_repo_mock: ProductsRepoMock,
        default_product_to_build: DBProductBuilder,
        carts_repo_mock: CartsRepoMock,
        default_user_to_build: DBUserBuilder,
        default_cart_built: DBCartInfoDTO,
        default_cart_resp_built: CartRespDTO,
        cart_service: CartService,
    ) -> None:
        requester: DBUserDTO = default_user_to_build.build()
        repo_cart: DBCartInfoDTO = default_cart_built

        carts_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=carts_repo_mock,
            attribute="get",
            return_value=repo_cart,
        )
        # NB: call of nested(!) service method was mocked
        products_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=products_repo_mock,
            attribute="get",
            side_effect=lambda idx, _: default_product_to_build.but()
            .with_id(idx)
            .build(),
        )
        expected = default_cart_resp_built
        received = await cart_service.get(requester.email, self.TEST_SHOP_ID)

        assert received == expected
        carts_repo_get_mocked.assert_awaited_once_with(requester.email)
        products_repo_get_mocked.assert_has_awaits(
            [
                call(item.product_id, self.TEST_SHOP_ID)
                for item in default_cart_built.products
            ]
        )

    async def test_get_london_school(
        self,
        mocker: MockerFixture,
        carts_repo_mock: CartsRepoMock,
        default_user_to_build: DBUserBuilder,
        default_cart_built: DBCartInfoDTO,
        default_cart_resp_built: CartRespDTO,
        default_products_list_s3_patched_built: ShopProductsListDTO,
        products_service: ProductsService,
        cart_service: CartService,
    ) -> None:
        requester: DBUserDTO = default_user_to_build.build()
        repo_cart: DBCartInfoDTO = default_cart_built
        svc_products = default_products_list_s3_patched_built.products

        carts_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=carts_repo_mock,
            attribute="get",
            return_value=repo_cart,
        )
        # NB: call of service method was mocked
        products_svc_get_mocked: AsyncMock = mocker.patch.object(
            target=products_service,
            attribute="get",
            side_effect=lambda idx, _: svc_products[idx - 1],
        )

        expected = default_cart_resp_built
        received = await cart_service.get(requester.email, self.TEST_SHOP_ID)

        assert received == expected
        carts_repo_get_mocked.assert_awaited_once_with(requester.email)
        products_svc_get_mocked.assert_has_awaits(
            [call(p.product_id, self.TEST_SHOP_ID) for p in repo_cart.products]
        )

    async def test_clear(
        self,
        mocker: MockerFixture,
        carts_repo_mock: CartsRepoMock,
        products_service,
        default_user_to_build: DBUserBuilder,
        cart_service: CartService,
    ) -> None:
        test_removed_items = 5
        requester: DBUserDTO = default_user_to_build.build()

        carts_repo_clear_mocked: AsyncMock = mocker.patch.object(
            target=carts_repo_mock,
            attribute="clear_cart",
            return_value=test_removed_items,
        )
        expected = test_removed_items
        received = await cart_service.clear_cart(requester.email)

        assert received == expected
        carts_repo_clear_mocked.assert_awaited_once_with(requester.email)
