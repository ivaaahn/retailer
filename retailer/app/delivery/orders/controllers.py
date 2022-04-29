from datetime import datetime

from fastapi import Depends, APIRouter, Query

from app.delivery.orders.deps import order_paging_params
from app.dto.orders import (
    OrderRespDTO,
    OrderStatusEnum,
    OrderReceiveKindEnum,
    OrdersListRespDTO,
    OrderListPagingParams,
    PlaceOrderRespDTO,
)
from app.dto.products import ShopProductDTO

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("", response_model=OrderRespDTO)
async def get(id: int) -> OrderRespDTO:
    return OrderRespDTO(
        id=1,
        products=[
            ShopProductDTO(
                id=1,
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                price=88.5,
                qty=30,
            ),
            ShopProductDTO(
                id=3, name="Морковь по корейски", category="закуски", price=99, qty=10
            ),
        ],
        status=OrderStatusEnum.created,
        created_at=datetime(2022, 4, 25, 3, 8, 45, 109647),
        receive_kind=OrderReceiveKindEnum.takeaway,
        total_price=187.5,
    )


@router.get(".list", response_model=OrdersListRespDTO)
async def get_list(
    paging_params: OrderListPagingParams = Depends(order_paging_params),
) -> OrdersListRespDTO:
    return OrdersListRespDTO(
        orders=[
            OrderRespDTO(
                id=1,
                products=[
                    ShopProductDTO(
                        id=1,
                        name="молоко",
                        description="годен 3 дня после открытия",
                        category="молочные продукты",
                        price=88.5,
                        qty=30,
                    ),
                    ShopProductDTO(
                        id=2, name="кока-кола", category="напитки", price=99, qty=10
                    ),
                ],
                status=OrderStatusEnum.created,
                created_at=datetime(2022, 4, 25, 3, 8, 45, 109647),
                receive_kind=OrderReceiveKindEnum.takeaway,
                total_price=187.5,
            )
        ],
        total=1,
    )


@router.put("")
async def place_order(
    shop_id: int,
    receive_kind: OrderReceiveKindEnum = Query(default=OrderReceiveKindEnum.takeaway),
) -> PlaceOrderRespDTO:
    return PlaceOrderRespDTO(order_id=1)
