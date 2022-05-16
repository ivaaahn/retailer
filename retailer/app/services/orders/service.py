from dataclasses import asdict

from fastapi import Depends

from app.base.services import BaseService
from app.delivery.orders.deps import order_paging_params
from app.delivery.orders.errors import OrderNotFoundError
from app.dto.api.orders import OrderRespDTO, OrdersListRespDTO, OrderListPagingParams
from app.repos.orders.implementation import OrdersRepo
from app.repos.orders.interface import IOrdersRepo


class OrdersService(BaseService):
    def __init__(self, orders_repo: IOrdersRepo = Depends(OrdersRepo)):
        super().__init__()
        self._orders_repo = orders_repo

    async def get(self, id: int) -> OrderRespDTO:
        order = await self._orders_repo.get(id)
        if not order:
            raise OrderNotFoundError(id)
        return OrderRespDTO(**asdict(order))

    async def get_list(
        self,
        paging_params: OrderListPagingParams = Depends(order_paging_params),
    ) -> OrdersListRespDTO:
        orders_list = await self._orders_repo.get_list(paging_params)
        return OrdersListRespDTO(**asdict(orders_list))
