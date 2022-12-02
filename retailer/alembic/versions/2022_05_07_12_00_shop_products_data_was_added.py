"""shop_products data was added

Revision ID: 7g1856998bb3
Revises: 6f1856998bb3
Create Date: 2022-05-05 21:18:53.575227

"""
import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Float, text

from scripts.faker.shop_products import generate, ShopProduct

revision = "7g1856998bb3"
down_revision = "6f1856998bb3"
branch_labels = None
depends_on = None


def upgrade():
    pass
    #
    # shop_products_table = table(
    #     "shop_products",
    #     column("id", Integer),
    #     column("shop_id", Integer),
    #     column("product_id", Integer),
    #     column("price", Float),
    #     column("qty", Integer),
    # )
    #
    # shop_products: list[ShopProduct] = generate()
    #
    # try:
    #     op.bulk_insert(
    #         shop_products_table,
    #         [asdict(shop_product) for shop_product in shop_products],
    #     )
    #     op.get_bind().execute(
    #         text(
    #             "SELECT SETVAL('shop_products_id_seq', COALESCE(MAX(id), 1) ) FROM shop_products;"
    #         )
    #     )
    #
    # except Exception as err:
    #     logging.warning(f"Error with shop_products' data insertion: {err}")
    #     raise


def downgrade():
    pass
