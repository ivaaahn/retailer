"""shops addresses data was added

Revision ID: 6396f15cadeb
Revises: 59ca10a9bd19
Create Date: 2022-04-03 01:59:52.646140

"""
import logging

from alembic import op
from sqlalchemy import column, table, Integer, Text

from scripts.faker.rw import read

revision = "6396f15cadeb"
down_revision = "59ca10a9bd19"
branch_labels = None
depends_on = None

SHOPS_ADDRESSES_CSV = "scripts/faker/data/shop_addresses.csv"


def upgrade():
    addresses_table = table(
        "shop_addresses",
        column("id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("building", Text),
        column("floor", Integer),
    )

    try:
        op.bulk_insert(
            addresses_table,
            [
                {
                    "city": item["city"],
                    "street": item["street"],
                    "house": item["house"],
                    "building": item["building"],
                    "floor": int(item["floor"]) if item["floor"] else None,
                }
                for item in read(SHOPS_ADDRESSES_CSV)
            ],
        )
    except Exception as err:
        logging.warning(f"Error with shop addresses data insertion: {err}")
        raise


def downgrade():
    pass
