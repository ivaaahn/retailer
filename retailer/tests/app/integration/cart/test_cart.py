from aioredis import Redis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from retailer.app.dto.db.products import DBCartInfoDTO, DBCartProductDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.misc import make_cart_key
from retailer.tests.builders.db.cart_product import CartApiBuilder
from retailer.tests.builders.db.product import (
    DBShopProductBuilder,
    save_shop_product,
)
from retailer.tests.builders.db.shops import DBShopBuilder
from retailer.tests.builders.db.user import save_user


class TestCart:
    URI = "api/cart"

    async def test_patch_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_active_user: DBUserDTO,
        auth_headers_default: dict[str, str],
        default_shop_to_build: DBShopBuilder,
        default_product_to_build: DBShopProductBuilder,
        cart_api_builder: CartApiBuilder,
        redis_cli: Redis,
    ) -> None:
        shop_product = default_product_to_build.but().with_photo(None).build()
        shop = default_shop_to_build.build()

        async with engine.begin() as conn:
            user = await save_user(conn, default_active_user)
            shop, shop_product = await save_shop_product(
                conn, shop_product, shop
            )

        qty_to_add = 2
        cart_api_builder.add_product(shop_product, qty_to_add)

        response = await cli.patch(
            self.URI,
            params={
                "shop_id": shop.id,
                "product_id": shop_product.product_id,
                "qty": qty_to_add,
            },
            headers=auth_headers_default,
        )
        assert response.is_success

        expected_response_api = cart_api_builder.build_response()
        received_response_api = response.json()
        assert received_response_api == expected_response_api

        expected_response_db = DBCartInfoDTO(
            products=[DBCartProductDTO(shop_product.product_id, qty_to_add)]
        )
        user_cart_db_raw = await redis_cli.hgetall(make_cart_key(user.email))
        received_response_db = DBCartInfoDTO.from_redis(user_cart_db_raw)
        assert received_response_db == expected_response_db
