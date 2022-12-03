from dataclasses import asdict

import pytest

from retailer.app.dto.api.orders import OrderRespDTO
from retailer.app.dto.api.products import ShopProductsListDTO
from retailer.app.dto.db.products import DBShopProductListDTO
from retailer.app.services.carts import CartService
from retailer.app.services.orders.service import OrdersService
from retailer.tests.builders.db.order import DBOrderProductsBuilder
from retailer.tests.mocks import RMQInteractionRepoMock
from retailer.tests.mocks.repo.orders import OrdersRepoMock


@pytest.fixture
def default_order_to_build(
    default_products_list_built: DBShopProductListDTO,
) -> DBOrderProductsBuilder:
    return DBOrderProductsBuilder().with_products(
        default_products_list_built.products
    )


@pytest.fixture
def default_order_s3_patched_built(
    default_order_to_build: DBOrderProductsBuilder,
    default_products_list_s3_patched_built: ShopProductsListDTO,
) -> OrderRespDTO:
    built = default_order_to_build.build()
    built.products = default_products_list_s3_patched_built.products
    return OrderRespDTO(**asdict(built))


@pytest.fixture
def orders_service(
    orders_repo_mock: OrdersRepoMock,
    rmq_interaction_repo_mock: RMQInteractionRepoMock,
    cart_service: CartService,
) -> OrdersService:
    return OrdersService(
        orders_repo_mock,
        cart_service,
        rmq_interaction_repo_mock,
    )
