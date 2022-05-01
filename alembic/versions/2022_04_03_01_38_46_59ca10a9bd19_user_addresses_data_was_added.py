"""user addresses data was added

Revision ID: 59ca10a9bd19
Revises: 39f94d3d830d
Create Date: 2022-04-03 01:38:46.429157

"""
import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Text

from scripts.faker.user_addresses import UserAddress, generate as generate_addresses

revision = "59ca10a9bd19"
down_revision = "39f94d3d830d"
branch_labels = None
depends_on = None


def upgrade():
    addresses_table = table(
        "addresses",
        column("id", Integer),
        column("user_id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("entrance", Integer),
        column("floor", Integer),
        column("flat", Text),
    )

    addresses: list[UserAddress] = generate_addresses()

    try:
        op.bulk_insert(
            addresses_table,
            [asdict(address) for address in addresses],
        )
    except Exception as err:
        logging.warning(f"Error with addresses' data insertion: {err}")
        raise


def downgrade():
    pass
