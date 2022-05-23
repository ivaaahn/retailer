from fastapi import Depends, APIRouter

from app.delivery.auth.deps import get_current_active_user
from app.delivery.orders.deps import order_paging_params
from app.dto.api.orders import (
    OrderRespDTO,
    OrdersListRespDTO,
    OrderListPagingParams,
    PlaceOrderRespDTO,
    PlaceOrderReqDTO,
)
from app.dto.api.user import UserRespDTO
from app.services.orders.service import OrdersService

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get("", response_model=OrderRespDTO)
async def get(
    id: int,
    order_service: OrdersService = Depends(),
) -> OrderRespDTO:
    return await order_service.get(id)


@router.get(".list", response_model=OrdersListRespDTO)
async def get_list(
    order_service: OrdersService = Depends(),
    user: UserRespDTO = Depends(get_current_active_user),
    paging_params: OrderListPagingParams = Depends(order_paging_params),
) -> OrdersListRespDTO:
    return await order_service.get_list(
        user,
        paging_params,
    )


@router.put("")
async def place_order(
    data: PlaceOrderReqDTO,
    order_service: OrdersService = Depends(),
    user: UserRespDTO = Depends(get_current_active_user),
) -> PlaceOrderRespDTO:
    return await order_service.place_order(data=data, user=user)
