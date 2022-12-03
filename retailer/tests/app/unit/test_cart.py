from unittest.mock import AsyncMock, call

import pytest
from pytest_mock import MockerFixture

from retailer.app.dto.api.cart import CartRespDTO
from retailer.app.dto.api.products import ShopProductsListDTO
from retailer.app.dto.db.products import DBCartInfoDTO, DBCartProductDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.services import ProductsService
from retailer.app.services.carts import CartService
from retailer.tests.builders.db.product import DBProductBuilder
from retailer.tests.builders.db.user import DBUserBuilder
from retailer.tests.mocks import ProductsRepoMock
from retailer.tests.mocks.repo.carts import CartsRepoMock


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
        # NB: call of nested(!) repo method was mocked
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

    async def test_update_to_zero(
        self,
        mocker: MockerFixture,
        carts_repo_mock: CartsRepoMock,
        default_user_to_build: DBUserBuilder,
        cart_service: CartService,
    ) -> None:
        requester: DBUserDTO = default_user_to_build.build()
        product_id = 1

        carts_repo_remove_mocked: AsyncMock = mocker.spy(
            obj=carts_repo_mock,
            name="remove",
        )

        await cart_service.update_cart(requester.email, product_id, 0)

        carts_repo_remove_mocked.assert_awaited_once_with(
            requester.email, product_id
        )

    async def test_update_to_non_zero(
        self,
        mocker: MockerFixture,
        carts_repo_mock: CartsRepoMock,
        default_user_to_build: DBUserBuilder,
        cart_service: CartService,
    ) -> None:
        requester: DBUserDTO = default_user_to_build.build()
        product_id = 1
        new_qty = 1

        carts_repo_add_to_cart_mocked: AsyncMock = mocker.spy(
            obj=carts_repo_mock,
            name="add_to_cart",
        )

        await cart_service.update_cart(requester.email, product_id, new_qty)

        carts_repo_add_to_cart_mocked.assert_awaited_once_with(
            requester.email, DBCartProductDTO(product_id, new_qty)
        )
