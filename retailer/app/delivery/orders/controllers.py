from datetime import datetime

from fastapi import Depends, APIRouter, Query

from app.delivery.auth.deps import get_current_active_user
from app.delivery.orders.deps import order_paging_params
from app.dto.api.orders import (
    OrderRespDTO,
    OrderStatusEnum,
    OrderReceiveKindEnum,
    OrdersListRespDTO,
    OrderListPagingParams,
    PlaceOrderRespDTO,
)
from app.dto.api.products import ShopProductDTO
from app.dto.api.user import UserRespDTO
from app.services.orders.service import OrdersService

router = APIRouter(
    prefix="/order",
    tags=["order"],
)


@router.get("", response_model=OrderRespDTO)
async def get(
    id: int,
    # user: UserRespDTO = Depends(get_current_active_user),
    order_service: OrdersService = Depends(),
) -> OrderRespDTO:
    return await order_service.get(id)


@router.get(".list", response_model=OrdersListRespDTO)
async def get_list(
    order_service: OrdersService = Depends(),
    paging_params: OrderListPagingParams = Depends(order_paging_params),
) -> OrdersListRespDTO:
    return await order_service.get_list(paging_params)


@router.put("")
async def place_order(
    shop_id: int,
    user: UserRespDTO = Depends(get_current_active_user),
    receive_kind: OrderReceiveKindEnum = Query(default=OrderReceiveKindEnum.takeaway),
) -> PlaceOrderRespDTO:
    return PlaceOrderRespDTO(order_id=1)
