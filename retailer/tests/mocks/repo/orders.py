import pytest

from retailer.app.base.repo import BasePgRepo
from retailer.app.dto.api.cart import CartRespDTO
from retailer.app.dto.api.orders import OrderListPagingParams
from retailer.app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
)
from retailer.app.models.orders import OrderReceiveKindEnum
from retailer.app.services.orders.interface import IOrdersRepo
from retailer.store import PgAccessor
from retailer.store.pg.config import PgConfig


class OrdersRepoMock(IOrdersRepo, BasePgRepo):
    async def get(self, order_id: int) -> DBOrderProductsDTO:
        pass

    async def get_list(
        self, user_id: int, paging_params: OrderListPagingParams
    ) -> DBOrderProductsListDTO:
        pass

    async def create(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        cart: CartRespDTO,
    ) -> int:
        pass


@pytest.fixture
def orders_repo_mock() -> OrdersRepoMock:
    return OrdersRepoMock(PgAccessor(PgConfig()))
