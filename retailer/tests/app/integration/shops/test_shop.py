from dataclasses import asdict

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine

from retailer.tests.builders.db.shops import DBShopBuilder, save_shop


class TestShop:
    URI = "api/shops"

    async def test_get_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_shop_to_build: DBShopBuilder,
    ) -> None:
        async with engine.begin() as conn:
            shop = await save_shop(conn, default_shop_to_build.build())

        response = await cli.get(self.URI, params={"shop_id": shop.id})
        assert response.is_success

        expected_data = {"shops": [asdict(shop)], "total": 1}
        received_data = response.json()
        assert received_data == expected_data
