from fastapi import Query, Depends

from app.base.repo import BasePgRepo
from app.delivery.orders.deps import order_paging_params
from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
    DBPlaceOrderDTO,
)
from app.dto.db.products import DBCartInfoDTO
from app.models.orders import OrderReceiveKindEnum
from app.repos.orders.interface import IOrdersRepo


class OrdersRepo(IOrdersRepo, BasePgRepo):
    async def get(self, id: int) -> DBOrderProductsDTO:
        pass

    async def get_list(
        self,
        paging_params: OrderListPagingParams = Depends(order_paging_params),
    ) -> DBOrderProductsListDTO:
        pass

    async def place_order(
        self,
        shop_id: int,
        cart: DBCartInfoDTO,
        email: str,
        receive_kind: OrderReceiveKindEnum = Query(
            default=OrderReceiveKindEnum.takeaway
        ),
    ) -> DBPlaceOrderDTO:
        pass
