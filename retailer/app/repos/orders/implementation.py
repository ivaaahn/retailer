from fastapi import Depends
from sqlalchemy import insert, func

from app.base.repo import BasePgRepo
from app.delivery.orders.deps import order_paging_params
from app.delivery.orders.errors import OrderNotFoundError
from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
    DBOrdersDTO,
)
from app.dto.db.products import DBShopProductDTO
from app.models.order_products import OrderProductsModel
from app.models.orders import OrderReceiveKindEnum, OrderModel
from app.models.product_categories import ProductCategoryModel
from app.models.products import ProductModel
from app.repos.orders.interface import IOrdersRepo
from sqlalchemy.future import select

__all__ = ("OrdersRepo",)


class OrdersRepo(IOrdersRepo, BasePgRepo):
    async def get(self, id: int) -> DBOrderProductsDTO:
        pt = ProductModel.__table__
        ord = OrderModel.__table__
        ordpt = OrderProductsModel.__table__
        ct = ProductCategoryModel.__table__

        stmt_order = (
            select(ord, ordpt)
            .where(ordpt.c.order_id == id)
            .select_from(ordpt.join(ord))
        )

        order = await self.get_one(stmt_order)
        if not order:
            raise OrderNotFoundError(id)

        stmt_products = (
            select(pt, ordpt, ct)
            .where(ordpt.c.order_id == id)
            .select_from(ordpt.join(pt).join(ct))
        )

        products = await self._execute(stmt_products)

        return DBOrderProductsDTO(
            id=order.id,
            total_price=order.total_price,
            receive_kind=order.receive_kind.value,
            status=order.status,
            created_at=order.created_at,
            products=[
                DBShopProductDTO(
                    id=product.id,
                    photo=product.photo,
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category=product.product_categories_name,
                    availability=product.order_products_qty,
                )
                for product in products
            ],
        )

    async def get_list(
        self,
        user_id: int,
        paging_params: OrderListPagingParams = Depends(order_paging_params),
    ) -> DBOrderProductsListDTO:
        ord = OrderModel.__table__

        stmt_order = select(ord).where(ord.c.user_id == user_id).select_from(ord)

        query = self.with_pagination(
            query=stmt_order,
            count=paging_params.count,
            offset=paging_params.offset,
            order=paging_params.order,
            sort=getattr(ord.c, paging_params.sort_by.value),
        )

        cursor_orders = await self._execute(query)

        stmt_total = (
            select(func.count()).where(ord.c.user_id == user_id).select_from(ord)
        )
        cursor_total = await self._execute(stmt_total)
        total = cursor_total.scalar()

        return DBOrderProductsListDTO(
            [
                DBOrdersDTO(
                    id=order.id,
                    total_price=order.total_price,
                    receive_kind=order.receive_kind.value,
                    status=order.status,
                    created_at=order.created_at,
                )
                for order in cursor_orders
            ],
            total,
        )

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
