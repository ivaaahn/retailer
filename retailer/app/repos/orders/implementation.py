from fastapi import Depends
from sqlalchemy import insert

from app.base.repo import BasePgRepo
from app.delivery.orders.deps import order_paging_params
from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
)
from app.models.order_products import OrderProductsModel
from app.models.orders import OrderReceiveKindEnum, OrderModel
from app.repos.orders.interface import IOrdersRepo


class OrdersRepo(IOrdersRepo, BasePgRepo):
    async def get(self, id: int) -> DBOrderProductsDTO:
        pass

    async def get_list(
        self,
        paging_params: OrderListPagingParams = Depends(order_paging_params),
    ) -> DBOrderProductsListDTO:
        pass

    async def create_order(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        total_price: float,
    ) -> int:
        order_t = OrderModel.__table__

        stmt = insert(order_t).values(
            shop_id=shop_id,
            address_id=address_id,
            receive_kind=receive_kind,
            user_id=user_id,
            total_price=total_price,
        )

        order_id = await self.execute_with_pk(stmt)

        return order_id

    @staticmethod
    def _cart2order_data(order_id: int, cart: CartRespDTO) -> list[dict]:
        return [
            {
                "order_id": order_id,
                "product_id": cart_item.product.id,
                "price": cart_item.product.price,
                "qty": cart_item.qty,
            }
            for cart_item in cart.products
        ]

    async def fill_order_with_products(
        self,
        order_id: int,
        cart: CartRespDTO,
    ) -> None:
        data_to_insert = self._cart2order_data(order_id, cart)
        order_product_t = OrderProductsModel.__table__
        await self._execute(insert(order_product_t), parameters=data_to_insert)
