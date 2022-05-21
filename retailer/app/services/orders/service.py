from dataclasses import asdict

from fastapi import Depends, Query

from app.base.services import BaseService
from app.delivery.orders.deps import order_paging_params
from app.delivery.orders.errors import OrderNotFoundError
from app.dto.api.orders import (
    OrderRespDTO,
    OrdersListRespDTO,
    OrderListPagingParams,
    PlaceOrderRespDTO,
)
from app.dto.db.products import DBCartInfoDTO
from app.models.orders import OrderReceiveKindEnum
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

    async def place_order(
        self,
        cart: DBCartInfoDTO,
        shop_id: int,
        email: str,
        receive_kind: OrderReceiveKindEnum = Query(
            default=OrderReceiveKindEnum.takeaway
        ),
    ) -> PlaceOrderRespDTO:
        order_id = await self._orders_repo.place_order(
            shop_id, cart, email, receive_kind
        )
        return PlaceOrderRespDTO(order_id=order_id)
