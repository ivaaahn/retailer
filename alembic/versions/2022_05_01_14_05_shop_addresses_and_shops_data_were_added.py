"""shop_addresses and shops data were added

Revision ID: 2dc1991f1701
Revises: 3dc8529d8689
Create Date: 2022-05-01 14:05:42.488215

"""
import logging
from dataclasses import asdict

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import column, table, Integer, Text

from scripts.faker.shops import generate as generate_shops, Shop
from scripts.faker.shops_addresses import ShopAddress, generate as generate_addresses

revision = "2dc1991f1701"
down_revision = "3dc8529d8689"
branch_labels = None
depends_on = None


def upgrade():
    shops_addresses_table = table(
        "shops_addresses",
        column("id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("floor", Integer),
    )

    shops_addresses: list[ShopAddress] = generate_addresses()

    shops_table = table(
        "shops",
        column("id", Integer),
        column("address_id", Integer),
    )

    shops: list[Shop] = generate_shops()

    try:
        op.bulk_insert(
            shops_addresses_table,
            [asdict(address) for address in shops_addresses],
        )
        op.bulk_insert(
            shops_table,
            [asdict(shop) for shop in shops],
        )
    except Exception as err:
        logging.warning(f"Error with shop' data insertion: {err}")
        raise


def downgrade():
    pass
