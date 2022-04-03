"""shops addresses data was added

Revision ID: 6396f15cadeb
Revises: 49f94d3d830d
Create Date: 2022-04-03 01:59:52.646140

"""
import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Text

from scripts.faker.shops import Shop, generate as generate_shop

revision = "6396f15cadeb"
down_revision = "49f94d3d830d"
branch_labels = None
depends_on = None


def upgrade():
    addresses_table = table(
        "shops",
        column("id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("building", Text),
        column("floor", Integer),
    )

    shops: list[Shop] = generate_shop(count=100)

    try:
        op.bulk_insert(
            addresses_table,
            [asdict(address) for address in shops],
        )
    except Exception as err:
        logging.warning(f"Error with shops' data insertion: {err}")
        raise


def downgrade():
    pass
