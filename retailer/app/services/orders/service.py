from dataclasses import asdict

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.base.errors import PostgresError, check_err, DBErrEnum
from app.base.services import BaseService
from app.delivery.orders.deps import order_paging_params
from app.delivery.orders.errors import (
    OrderNotFoundError,
    NoProductsInCartError,
    ProductTemporarilyUnavailable,
)
from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import (
    OrderRespDTO,
    OrdersListRespDTO,
    OrderListPagingParams,
    PlaceOrderRespDTO,
    PlaceOrderReqDTO,
)
from app.dto.api.user import UserRespDTO
from app.repos.cart.implementation import CartsRepo
from app.repos.cart.interface import ICartsRepo
from app.repos.orders.implementation import OrdersRepo
from app.repos.orders.interface import IOrdersRepo
from app.repos.products import IProductsRepo, ProductsRepo
from app.services.carts import CartService
from store.pg.accessor import pg_accessor


class OrdersService(BaseService):
    def __init__(
        self,
        orders_repo: IOrdersRepo = Depends(OrdersRepo),
        cart_service: CartService = Depends(),
        carts_repo: ICartsRepo = Depends(CartsRepo),
        products_repo: IProductsRepo = Depends(ProductsRepo),
    ):
        super().__init__()
        self._carts_repo = carts_repo
        self._orders_repo = orders_repo
        self._products_repo = products_repo
        self._cart_service = cart_service

    async def get(self, id: int) -> OrderRespDTO:
        order = await self._orders_repo.get(id)
        if not order:
            raise OrderNotFoundError(id)
        return OrderRespDTO(**asdict(order))

    async def get_list(
        self,
        user: UserRespDTO,
        paging_params: OrderListPagingParams = Depends(order_paging_params),
    ) -> OrdersListRespDTO:
        orders_list = await self._orders_repo.get_list(
            user.id,
            paging_params,
        )
        return OrdersListRespDTO(**asdict(orders_list))

    async def _create_and_fill_order(
        self, user: UserRespDTO, data: PlaceOrderReqDTO, cart: CartRespDTO
    ) -> int:
        order_id = await self._orders_repo.create_order(
            user_id=user.id,
            shop_id=data.shop_id,
            address_id=data.delivery_address_id,
            receive_kind=data.receive_kind,
            total_price=cart.total_price,
        )

        await self._orders_repo.fill_order_with_products(order_id=order_id, cart=cart)

        return order_id

    async def place_order(
        self,
        data: PlaceOrderReqDTO,
        user: UserRespDTO,
    ) -> PlaceOrderRespDTO:
        cart: CartRespDTO = await self._cart_service.get(user.email, data.shop_id)

        if not cart.products:
            raise NoProductsInCartError()

        try:
            async with pg_accessor.acquire():
                order_id = await self._create_and_fill_order(user, data, cart)
                await self._products_repo.reduce_qty(data.shop_id, cart)
        except IntegrityError as err:
            if check_err(err, DBErrEnum.check_violation):
                raise ProductTemporarilyUnavailable(*err.params[1:])
            raise PostgresError(description=str(err))
        except Exception as err:
            raise PostgresError(description=str(err))
        else:
            await self._cart_service.clear_cart(user.email)

        # todo payment

        return PlaceOrderRespDTO(order_id=order_id)
