from dataclasses import asdict

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.base.errors import DBErrEnum, PostgresError, check_err
from app.base.services import BaseService
from app.delivery.orders.deps import order_paging_params
from app.delivery.orders.errors import (
    NoProductsInCartError,
    OrderNotFoundError,
    ProductTemporarilyUnavailable,
)
from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import (
    OrderListPagingParams,
    OrderRespDTO,
    OrdersListRespDTO,
    PlaceOrderReqDTO,
    PlaceOrderRespDTO,
)
from app.dto.api.products import ShopProductDTO
from app.dto.api.profile import AddressDTO
from app.dto.api.user import UserRespDTO
from app.repos import IRMQInteractRepo, RMQInteractRepo
from app.repos.cart.implementation import CartsRepo
from app.repos.cart.interface import ICartsRepo
from app.repos.orders.implementation import OrdersRepo
from app.repos.orders.interface import IOrdersRepo
from app.services.carts import CartService


class OrdersService(BaseService):
    def __init__(
        self,
        orders_repo: IOrdersRepo = Depends(OrdersRepo),
        cart_service: CartService = Depends(),
        carts_repo: ICartsRepo = Depends(CartsRepo),
        rmq_repo: IRMQInteractRepo = Depends(RMQInteractRepo),
    ):
        super().__init__()
        self._carts_repo = carts_repo
        self._orders_repo = orders_repo
        self._cart_service = cart_service
        self._rmq_repo = rmq_repo

    @staticmethod
    def _make_s3_url(path: str) -> str:
        return f"/img/{path}" if path else None

    async def get(self, id: int) -> OrderRespDTO:
        order = await self._orders_repo.get(id)

        if not order:
            raise OrderNotFoundError(id)

        delivery_address = None
        if order.delivery_address:
            delivery_address = AddressDTO(**asdict(order.delivery_address))

        return OrderRespDTO(
            id=order.id,
            status=order.status,
            created_at=order.created_at,
            receive_kind=order.receive_kind,
            total_price=order.total_price,
            delivery_address=delivery_address,
            products=[
                ShopProductDTO(
                    id=product.id,
                    photo=self._make_s3_url(product.photo),
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category=product.category,
                    availability=product.availability,
                )
                for product in order.products
            ],
        )

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

    async def place_order(
        self,
        data: PlaceOrderReqDTO,
        user: UserRespDTO,
    ) -> PlaceOrderRespDTO:
        cart: CartRespDTO = await self._cart_service.get(user.email, data.shop_id)

        if not cart.products:
            raise NoProductsInCartError()

        try:
            order_id = await self._orders_repo.create(
                user_id=user.id,
                shop_id=data.shop_id,
                address_id=data.delivery_address_id,
                receive_kind=data.receive_kind,
                cart=cart,
            )
        except IntegrityError as err:
            check_err(
                err,
                exp_error=DBErrEnum.check_violation,
                raise_exc=ProductTemporarilyUnavailable(*err.params[1:]),
            )
            raise PostgresError(description=str(err))

        await self._rmq_repo.send_accept(user.email, order_id)
        await self._cart_service.clear_cart(user.email)

        # todo payment

        return PlaceOrderRespDTO(order_id=order_id)
