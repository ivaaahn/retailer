import pytest
from aioredis import Redis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.dto.db.products import DBShopProductDTO
from retailer.app.dto.db.shops import DBShopDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.misc import make_cart_key
from retailer.app.models.orders import (
    OrderModel,
    OrderReceiveKindEnum,
    OrderStatusEnum,
)
from retailer.app.services.auth.service import pwd_context
from retailer.store.rmq import RMQAccessor
from retailer.tests.builders.db.product import save_shop_product
from retailer.tests.builders.db.user import DBUserBuilder, save_user
from retailer.tests.constants import DEFAULT_DATETIME


class TestLoginAndPlaceOrder:
    LOGIN_URI = "api/auth/login"
    CART_URI = "api/cart"
    ORDER_URI = "api/orders"

    EMAIL = "test@test.com"
    PASSWORD = "test"
    CODE = "12345678"
    PRODUCTS_QTY = 1

    @pytest.mark.freeze_time(DEFAULT_DATETIME)
    async def test_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_user_to_build: DBUserBuilder,
        default_shop: DBShopDTO,
        default_product_no_photo: DBShopProductDTO,
        rabbit_cli: RMQAccessor,
        redis_cli: Redis,
    ) -> None:
        user, shop, shop_product = await self.__prepare_database(
            engine,
            default_user_to_build,
            default_shop,
            default_product_no_photo,
        )

        # 1. LOGIN
        login_response = await cli.post(
            self.LOGIN_URI,
            data={"username": self.EMAIL, "password": self.PASSWORD},
        )
        assert login_response.is_success

        access_token: str = login_response.json()["access_token"]
        auth_header = {"Authorization": f"Bearer {access_token}"}

        # 2. ADD PRODUCTS TO CART
        add_to_cart_response = await cli.patch(
            self.CART_URI,
            params={
                "shop_id": shop.id,
                "product_id": shop_product.product_id,
                "qty": self.PRODUCTS_QTY,
            },
            headers=auth_header,
        )
        assert add_to_cart_response.is_success

        # 3. PLACE ORDER
        place_order_response_api = await cli.put(
            self.ORDER_URI,
            json={"shop_id": shop.id},
            headers=auth_header,
        )
        assert place_order_response_api.is_success

        # PG STATE
        async with engine.begin() as conn:
            order_t = OrderModel.__table__
            cursor = await conn.execute(
                select(order_t).where(order_t.c.user_id == user.id)
            )

        order_db = dict(cursor.first())
        order_db.pop("created_at")

        expected_response_db = {
            "id": place_order_response_api.json()["order_id"],
            "user_id": user.id,
            "shop_id": shop.id,
            "total_price": shop_product.price * self.PRODUCTS_QTY,
            "receive_kind": OrderReceiveKindEnum.takeaway.value,
            "status": OrderStatusEnum.collecting.value,
            "address_id": None,
        }
        assert order_db == expected_response_db

        # RABBIT STATE
        expected_messages_count = 1
        received_message_count = await rabbit_cli.get_messages_count()
        assert received_message_count == expected_messages_count

        # REDIS STATE
        user_cart_db = await redis_cli.hgetall(make_cart_key(user.email))
        assert user_cart_db == {}

    async def __prepare_database(
        self,
        engine: AsyncEngine,
        user_to_build,
        shop: DBShopDTO,
        product: DBShopProductDTO,
    ) -> tuple[DBUserDTO, DBShopDTO, DBShopProductDTO]:
        async with engine.begin() as conn:
            user = await save_user(
                conn,
                user=(
                    user_to_build.but()
                    .with_email(self.EMAIL)
                    .with_password(pwd_context.hash(self.PASSWORD))
                    .with_is_active(True)
                    .build()
                ),
            )
            shop, shop_product = await save_shop_product(conn, product, shop)

            return user, shop, shop_product
