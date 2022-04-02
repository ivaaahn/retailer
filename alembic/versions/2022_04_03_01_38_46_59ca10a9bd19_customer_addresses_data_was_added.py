"""customer addresses data was added

Revision ID: 59ca10a9bd19
Revises: 39f94d3d830d
Create Date: 2022-04-03 01:38:46.429157

"""
import logging

from alembic import op
from sqlalchemy import column, table, Integer, Text

from scripts.faker.rw import read

revision = "59ca10a9bd19"
down_revision = "39f94d3d830d"
branch_labels = None
depends_on = None

CUSTOMER_ADDRESSES_CSV = "scripts/faker/data/customer_addresses.csv"


def upgrade():
    addresses_table = table(
        "customer_addresses",
        column("id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("entrance", Integer),
        column("floor", Integer),
        column("flat", Text),
    )

    try:
        op.bulk_insert(
            addresses_table,
            [
                {
                    "city": item["city"],
                    "street": item["street"],
                    "house": item["house"],
                    "entrance": int(item["entrance"]) if item["entrance"] else None,
                    "floor": int(item["floor"]) if item["floor"] else None,
                    "flat": item["flat"],
                }
                for item in read(CUSTOMER_ADDRESSES_CSV)
            ],
        )
    except Exception as err:
        logging.warning(f"Error with customer addresses data insertion: {err}")
        raise


def downgrade():
    pass
