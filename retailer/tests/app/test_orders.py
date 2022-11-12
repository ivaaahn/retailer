from unittest.mock import AsyncMock, MagicMock, call

import pytest
from pytest_mock import MockerFixture

from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderRespDTO, PlaceOrderReqDTO, PlaceOrderRespDTO
from app.dto.api.user import UserRespDTO
from app.dto.db.products import DBCartInfoDTO
from app.models.orders import OrderReceiveKindEnum
from app.services.carts import CartService
from app.services.orders.service import OrdersService
from tests.builders.db.order import DBOrderProductsBuilder
from tests.builders.db.product import DBProductBuilder
from tests.mocks import CartsRepoMock, RMQInteractionRepoMock
from tests.mocks.repo.products import ProductsRepoMock


class TestOrders:
    ORDER_ID_MOCKED = 1
    SHOP_ID_MOCKED = 1
    USER_ID_MOCKED = 1

    async def test_get(
        self,
        mocker: MockerFixture,
        orders_service: OrdersService,
        make_s3_url_mocked: MagicMock,
        orders_repo_mock: ProductsRepoMock,
        default_order_to_build: DBOrderProductsBuilder,
        default_order_s3_patched_built: OrderRespDTO,
    ) -> None:
        repo_order = default_order_to_build.build()

        orders_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=orders_repo_mock,
            attribute="get",
            return_value=repo_order,
        )

        expected = default_order_s3_patched_built
        received = await orders_service.get(repo_order.id)

        assert received == expected
        make_s3_url_mocked.assert_has_calls(
            [call(p.photo) for p in repo_order.products]
        )

        orders_repo_get_mocked.assert_awaited_once_with(repo_order.id)

    async def test_place_order_london(
        self,
        mocker: MockerFixture,
        orders_service: OrdersService,
        orders_repo_mock: ProductsRepoMock,
        default_cart_resp_built: CartRespDTO,
        default_order_to_build: DBOrderProductsBuilder,
        rmq_interaction_repo_mock: RMQInteractionRepoMock,
        cart_service: CartService,
        default_active_user_api: UserRespDTO,
    ) -> None:
        requester = default_active_user_api

        carts_service_get_mocked: AsyncMock = mocker.patch.object(
            target=cart_service,
            attribute="get",
            return_value=default_cart_resp_built,
        )
        orders_repo_create_mocked: AsyncMock = mocker.patch.object(
            target=orders_repo_mock,
            attribute="create",
            return_value=self.ORDER_ID_MOCKED,
        )
        rmq_repo_send_accept_mocked: AsyncMock = mocker.patch.object(
            target=rmq_interaction_repo_mock,
            attribute="send_accept",
        )
        cart_service_clear_mocked: AsyncMock = mocker.patch.object(
            target=cart_service,
            attribute="clear_cart",
        )

        expected = PlaceOrderRespDTO(order_id=self.ORDER_ID_MOCKED)
        received = await orders_service.place_order(
            data=PlaceOrderReqDTO(shop_id=self.SHOP_ID_MOCKED),
            user=requester,
        )

        assert received == expected
        carts_service_get_mocked.assert_awaited_once_with(
            requester.email, self.SHOP_ID_MOCKED
        )
        orders_repo_create_mocked.assert_awaited_once_with(
            user_id=requester.id,
            shop_id=self.SHOP_ID_MOCKED,
            address_id=None,
            receive_kind=OrderReceiveKindEnum.takeaway,
            cart=default_cart_resp_built,
        )
        rmq_repo_send_accept_mocked.assert_awaited_once_with(
            requester.email,
            self.ORDER_ID_MOCKED,
        )
        cart_service_clear_mocked.assert_awaited_once_with(requester.email)

    @pytest.mark.usefixtures("make_s3_url_mocked")
    async def test_place_order_classic(
        self,
        mocker: MockerFixture,
        orders_service: OrdersService,
        orders_repo_mock: ProductsRepoMock,
        default_cart_resp_built: CartRespDTO,
        default_order_to_build: DBOrderProductsBuilder,
        rmq_interaction_repo_mock: RMQInteractionRepoMock,
        cart_service: CartService,
        default_active_user_api: UserRespDTO,
        carts_repo_mock: CartsRepoMock,
        default_cart_built: DBCartInfoDTO,
        products_repo_mock: ProductsRepoMock,
        default_product_to_build: DBProductBuilder,
    ) -> None:
        requester = default_active_user_api
        repo_cart: DBCartInfoDTO = default_cart_built

        carts_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=carts_repo_mock,
            attribute="get",
            return_value=repo_cart,
        )
        products_repo_get_mocked: AsyncMock = mocker.patch.object(
            target=products_repo_mock,
            attribute="get",
            side_effect=lambda idx, _: default_product_to_build.but()
            .with_id(idx)
            .build(),
        )

        orders_repo_create_mocked: AsyncMock = mocker.patch.object(
            target=orders_repo_mock,
            attribute="create",
            return_value=self.ORDER_ID_MOCKED,
        )
        rmq_repo_send_accept_mocked: AsyncMock = mocker.patch.object(
            target=rmq_interaction_repo_mock,
            attribute="send_accept",
        )
        cart_service_clear_mocked: AsyncMock = mocker.patch.object(
            target=cart_service,
            attribute="clear_cart",
        )

        expected = PlaceOrderRespDTO(order_id=self.ORDER_ID_MOCKED)
        received = await orders_service.place_order(
            data=PlaceOrderReqDTO(shop_id=self.SHOP_ID_MOCKED),
            user=requester,
        )

        assert received == expected
        carts_repo_get_mocked.assert_awaited_once_with(requester.email)
        products_repo_get_mocked.assert_has_awaits(
            [
                call(item.product_id, self.SHOP_ID_MOCKED)
                for item in default_cart_built.products
            ]
        )
        orders_repo_create_mocked.assert_awaited_once_with(
            user_id=requester.id,
            shop_id=self.SHOP_ID_MOCKED,
            address_id=None,
            receive_kind=OrderReceiveKindEnum.takeaway,
            cart=default_cart_resp_built,
        )
        rmq_repo_send_accept_mocked.assert_awaited_once_with(
            requester.email,
            self.ORDER_ID_MOCKED,
        )
        cart_service_clear_mocked.assert_awaited_once_with(requester.email)
