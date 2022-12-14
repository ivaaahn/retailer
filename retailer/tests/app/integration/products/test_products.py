from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from retailer.tests.builders.db.product import (
    DBShopProductBuilder,
    save_shop_product,
)
from retailer.tests.builders.db.shops import DBShopBuilder


class TestProducts:
    URI = "api/products"

    async def test_get_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_shop_to_build: DBShopBuilder,
        default_product_to_build: DBShopProductBuilder,
    ) -> None:
        async with engine.begin() as conn:
            shop, shop_product = await save_shop_product(
                conn,
                shop=default_shop_to_build.build(),
                shop_product=default_product_to_build.but()
                .with_photo(None)
                .build(),
            )

        response = await cli.get(
            f"{self.URI}/{shop_product.product_id}",
            params={"shop_id": shop_product.shop_id},
        )
        assert response.is_success

        received_data = response.json()
        expected_data = shop_product.to_dict()
        assert received_data == expected_data
