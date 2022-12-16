from aioredis import Redis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.dto.db.products import DBShopProductDTO
from retailer.app.dto.db.shops import DBShopDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.misc import make_cart_key, make_product_key
from retailer.app.models.orders import (
    OrderModel,
    OrderReceiveKindEnum,
    OrderStatusEnum,
)
from retailer.store.rmq import RMQAccessor
from retailer.tests.builders.db.order import DBOrderProductsBuilder
from retailer.tests.builders.db.product import save_shop_product
from retailer.tests.builders.db.user import save_user


class TestOrders:
    URI = "api/orders"

    async def test_put_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_active_user: DBUserDTO,
        auth_headers_default: dict[str, str],
        default_shop: DBShopDTO,
        default_product_no_photo: DBShopProductDTO,
        default_order_to_build: DBOrderProductsBuilder,
        redis_cli: Redis,
        rabbit_cli: RMQAccessor,
    ) -> None:
        qty_to_add = 2
        async with engine.begin() as conn:
            user = await save_user(conn, default_active_user)
            shop, shop_product = await save_shop_product(
                conn, default_product_no_photo, default_shop
            )
        await redis_cli.hset(
            name=make_cart_key(user.email),
            key=make_product_key(shop_product.product_id),
            value=qty_to_add,
        )

        response = await cli.put(
            self.URI,
            json={"shop_id": shop.id},
            headers=auth_headers_default,
        )
        assert response.is_success
        expected_messages_count = 1
        received_message_count = await rabbit_cli.get_messages_count()
        assert received_message_count == expected_messages_count

        async with engine.begin() as conn:
            order_t = OrderModel.__table__
            cursor = await conn.execute(
                select(order_t).where(order_t.c.user_id == user.id)
            )

        received_response_api = response.json()
        received_response_db = dict(cursor.first())
        received_response_db.pop("created_at")
        assert received_response_api["order_id"] == received_response_db["id"]

        expected_response_db = {
            "id": 1,
            "user_id": user.id,
            "shop_id": shop.id,
            "total_price": shop_product.price * qty_to_add,
            "receive_kind": OrderReceiveKindEnum.takeaway.value,
            "status": OrderStatusEnum.collecting.value,
            "address_id": None,
        }
        assert received_response_db == expected_response_db
