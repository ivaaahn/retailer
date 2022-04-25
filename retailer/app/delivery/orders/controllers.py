from datetime import datetime

from fastapi import Depends, APIRouter, Query

from app.delivery.orders.deps import order_paging_params
from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.orders import (
    OrderRespDTO,
    OrderStatusEnum,
    OrderReceiveKindEnum,
    OrderListRespDTO,
    OrderListPagingParams,
)
from app.dto.products import ProductListRespDTO, ProductRespDTO

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.get("", response_model=OrderRespDTO)
async def get_by_shop(order_id: int) -> OrderRespDTO:
    return OrderRespDTO(
        id=1,
        products=[
            ProductRespDTO(
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                price=88.5,
                qty=30,
            ),
            ProductRespDTO(name="Морковь по корейски", category="закуски", price=99, qty=10),
        ],
        status=OrderStatusEnum.created,
        created_at=datetime(2022, 4, 25, 3, 8, 45, 109647),
        receive_kind=OrderReceiveKindEnum.take_away,
        summ=187.5,
    )


@router.get(".list", response_model=OrderListRespDTO)
async def get_list(
    paging_params: OrderListPagingParams = Depends(order_paging_params),
) -> OrderListRespDTO:
    return OrderListRespDTO(
        order=[
            OrderRespDTO(
                id=1,
                products=[
                    ProductRespDTO(
                        name="молоко",
                        description="годен 3 дня после открытия",
                        category="молочные продукты",
                        price=88.5,
                        qty=30,
                    ),
                    ProductRespDTO(
                        name="кока-кола", category="напитки", price=99, qty=10
                    ),
                ],
                status=OrderStatusEnum.created,
                created_at=datetime(2022, 4, 25, 3, 8, 45, 109647),
                receive_kind=OrderReceiveKindEnum.take_away,
                summ=187.5,
            )
        ],
        total=1,
    )


@router.put("")
async def place_order(
    shop_id: int,
    receive_kind: OrderReceiveKindEnum = Query(default=OrderReceiveKindEnum.take_away),
):
    return {"order_id": 1}
