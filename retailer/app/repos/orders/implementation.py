import asyncio
from asyncio import gather

from fastapi import Depends
from sqlalchemy import and_, func, insert, update
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.delivery.orders.errors import OrderNotFoundError
from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.api.products import CartProductDTO
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
    DBOrdersDTO,
)
from app.dto.db.products import DBShopProductDTO
from app.dto.db.profile import DBAddressDTO
from app.models.order_products import OrderProductsModel
from app.models.orders import OrderModel, OrderReceiveKindEnum
from app.models.product_categories import ProductCategoryModel
from app.models.products import ProductModel
from app.models.shop_products import ShopProductsModel
from app.models.user_addresses import UserAddressModel
from app.repos.orders.interface import IOrdersRepo
from app.repos.products import IProductsRepo, ProductsRepo
from store import PgAccessor, pg_accessor

__all__ = ("OrdersRepo",)


class OrdersRepo(IOrdersRepo, BasePgRepo):
    def __init__(
        self,
        pg: PgAccessor = Depends(pg_accessor),
        products_repo: IProductsRepo = Depends(ProductsRepo),
    ):
        super(OrdersRepo, self).__init__(pg=pg)
        self._products_repo = products_repo

    async def get(self, order_id: int) -> DBOrderProductsDTO:
        order_cursor = await self.get_one(self._select_order_stmt(order_id))
        if not order_cursor:
            raise OrderNotFoundError(order_id)

        products_cursor, address_scalar = await gather(
            self._execute(self._select_order_products_stmt(order_id)),
            self.get_one(self._select_order_delivery_addr_stmt(order_id)),
        )
        return DBOrderProductsDTO(
            id=order_cursor.id,
            total_price=order_cursor.total_price,
            receive_kind=order_cursor.receive_kind,
            status=order_cursor.status,
            created_at=order_cursor.created_at,
            delivery_address=DBAddressDTO.from_db(address_scalar),
            products=[
                DBShopProductDTO.from_db(product_db) for product_db in products_cursor
            ],
        )

    async def get_list(
        self,
        user_id: int,
        paging_params: OrderListPagingParams,
    ) -> DBOrderProductsListDTO:
        orders_cursor, total = await gather(
            self._execute(self._select_orders_stmt(user_id, paging_params)),
            self.get_scalar(self._select_total_stmt(user_id))
        )

        return DBOrderProductsListDTO(
            orders=[DBOrdersDTO.from_db(order_db) for order_db in orders_cursor],
            total=total,
        )

    async def create(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        cart: CartRespDTO,
    ) -> int:
        insert_order_stmt = self._insert_order_stmt(
            shop_id=shop_id,
            address_id=address_id,
            receive_kind=receive_kind,
            user_id=user_id,
            total_price=cart.total_price,
        )
        insert_order_products_stmt = insert(OrderProductsModel.__table__)
        reduce_products_qty_stmt = self._reduce_product_qty_stmt(
            shop_id=shop_id, products=cart.products
        )

        execute = self._execute
        async with self._pg.engine.begin() as conn:
            order_id = await self.execute_with_pk(insert_order_stmt, conn=conn)
            queries = [
                execute(
                    insert_order_products_stmt,
                    parameters=self._cart2order_data(order_id, cart),
                    conn=conn,
                ),
                *[execute(stmt, conn=conn) for stmt in reduce_products_qty_stmt],
            ]
            await asyncio.gather(*queries)

        return order_id

    @staticmethod
    def _select_order_stmt(order_id: int):
        order_t = OrderModel.__table__
        order_product_t = OrderProductsModel.__table__
        return (
            select(order_t, order_product_t)
            .where(order_product_t.c.order_id == order_id)
            .select_from(order_product_t.join(order_t))
        )

    @staticmethod
    def _select_order_products_stmt(order_id: int):
        product_t = ProductModel.__table__
        order_product_t = OrderProductsModel.__table__
        product_category_t = ProductCategoryModel.__table__
        return (
            select(product_t, order_product_t, product_category_t)
            .where(order_product_t.c.order_id == order_id)
            .select_from(order_product_t.join(product_t).join(product_category_t))
        )

    @staticmethod
    def _select_order_delivery_addr_stmt(order_id: int):
        order_t = OrderModel.__table__
        user_address_t = UserAddressModel.__table__
        return (
            select(user_address_t)
            .where(order_t.c.id == order_id)
            .select_from(order_t.join(user_address_t))
        )

    @staticmethod
    def _insert_order_stmt(
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        user_id: int,
        total_price: float,
    ):
        return insert(OrderModel.__table__).values(
            shop_id=shop_id,
            address_id=address_id,
            receive_kind=receive_kind,
            user_id=user_id,
            total_price=total_price,
        )

    @staticmethod
    def _reduce_product_qty_stmt(shop_id: int, products: list[CartProductDTO]) -> list:
        shop_product_t = ShopProductsModel.__table__

        return [
            (
                update(shop_product_t)
                .where(
                    and_(
                        shop_product_t.c.product_id == cart_item.product.id,
                        shop_product_t.c.shop_id == shop_id,
                    )
                )
                .values(qty=shop_product_t.c.qty - cart_item.qty)
            )
            for cart_item in products
        ]

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

    def _select_orders_stmt(self, user_id: int, paging_params: OrderListPagingParams):
        order_t = OrderModel.__table__
        base_stmt = select(order_t).where(order_t.c.user_id == user_id)

        return self.with_pagination(
            query=base_stmt,
            count=paging_params.count,
            offset=paging_params.offset,
            order=paging_params.order,
            sort=getattr(OrderModel.__table__.c, paging_params.sort_by.value),
        )

    @staticmethod
    def _select_total_stmt(user_id: int):
        order_t = OrderModel.__table__
        return (
            select(func.count())
            .where(order_t.c.user_id == user_id)
            .select_from(order_t)
        )
