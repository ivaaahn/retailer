from dataclasses import asdict

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

import retailer.app.misc
from retailer.app.base.errors import DatabaseError, DBErrEnum, check_err
from retailer.app.base.services import BaseService
from retailer.app.delivery.orders.deps import order_paging_params
from retailer.app.delivery.orders.errors import (
    NoProductsInCartError,
    OrderNotFoundError,
    ProductTemporarilyUnavailable,
)
from retailer.app.dto.api.cart import CartRespDTO
from retailer.app.dto.api.orders import (
    OrderListPagingParams,
    OrderRespDTO,
    OrdersListRespDTO,
    PlaceOrderReqDTO,
    PlaceOrderRespDTO,
)
from retailer.app.dto.api.products import ShopProductDTO
from retailer.app.dto.api.profile import AddressRespDTO
from retailer.app.dto.api.user import UserRespDTO
from retailer.app.models.orders import OrderReceiveKindEnum, OrderStatusEnum
from retailer.app.repos.orders import OrdersRepo
from retailer.app.repos.rmq import RMQInteractRepo
from retailer.app.services.auth.interfaces import IRMQInteractRepo
from retailer.app.services.carts import CartService
from retailer.app.services.orders.interface import IOrdersRepo


class OrdersService(BaseService):
    def __init__(
        self,
        orders_repo: IOrdersRepo = Depends(OrdersRepo),
        cart_service: CartService = Depends(),
        rmq_repo: IRMQInteractRepo = Depends(RMQInteractRepo),
    ):
        super().__init__()
        self._orders_repo = orders_repo
        self._cart_service = cart_service
        self._rmq_repo = rmq_repo

    async def get(self, id: int) -> OrderRespDTO:
        order = await self._orders_repo.get(id)

        if not order:
            raise OrderNotFoundError(id)

        delivery_address = None
        if order.delivery_address:
            delivery_address = AddressRespDTO(**asdict(order.delivery_address))

        return OrderRespDTO(
            id=order.id,
            status=OrderStatusEnum(order.status),
            created_at=order.created_at,
            receive_kind=OrderReceiveKindEnum(order.receive_kind),
            total_price=order.total_price,
            delivery_address=delivery_address,
            products=[
                ShopProductDTO(
                    id=product.id,
                    photo=retailer.app.misc.make_s3_url(product.photo),
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
        self, data: PlaceOrderReqDTO, user: UserRespDTO
    ) -> PlaceOrderRespDTO:
        cart: CartRespDTO = await self._cart_service.get(
            user.email, data.shop_id
        )

        if not cart.products:
            raise NoProductsInCartError()

        try:
            order_id: int = await self._orders_repo.create(
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
            raise DatabaseError(description=str(err))

        await self._rmq_repo.send_accept(user.email, order_id)
        await self._cart_service.clear_cart(user.email)

        return PlaceOrderRespDTO(order_id=order_id)
