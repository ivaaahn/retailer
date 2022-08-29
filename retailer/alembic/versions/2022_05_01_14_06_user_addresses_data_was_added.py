"""user addresses data was added

Revision ID: 59ca10a9bd19
Revises: 2dc1991f1701
Create Date: 2022-04-03 01:38:46.429157

"""
import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Text, text

from scripts.faker.user_addresses import UserAddress, generate as generate_addresses

revision = "59ca10a9bd19"
down_revision = "2dc1991f1701"
branch_labels = None
depends_on = None


def upgrade():
    addresses_table = table(
        "user_addresses",
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
        op.get_bind().execute(text("SELECT SETVAL('user_addresses_id_seq', COALESCE(MAX(id), 1) ) FROM user_addresses;"))

    except Exception as err:
        logging.warning(f"Error with user addresses' data insertion: {err}")
        raise


def downgrade():
    pass
