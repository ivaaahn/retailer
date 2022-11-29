from dataclasses import asdict

import pytest
from app.dto.api.orders import OrderRespDTO
from app.dto.api.products import ShopProductsListDTO
from app.dto.db.products import DBShopProductListDTO
from app.services.carts import CartService
from app.services.orders.service import OrdersService
from tests.builders.db.order import DBOrderProductsBuilder
from tests.mocks import RMQInteractionRepoMock
from tests.mocks.repo.orders import OrdersRepoMock


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
