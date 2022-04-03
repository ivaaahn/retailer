"""customer addresses data was added

Revision ID: 59ca10a9bd19
Revises: ed5f34fdabb8
Create Date: 2022-04-03 01:38:46.429157

"""
import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Text

from scripts.faker.addresses import CustomerAddress, generate as generate_addresses

revision = "59ca10a9bd19"
down_revision = "ed5f34fdabb8"
branch_labels = None
depends_on = None


def upgrade():
    addresses_table = table(
        "customer_addresses",
        column("id", Integer),
        column("customer_id", Integer),
        column("city", Text),
        column("street", Text),
        column("house", Text),
        column("entrance", Integer),
        column("floor", Integer),
        column("flat", Text),
    )

    addresses: list[CustomerAddress] = generate_addresses(count=100)

    try:
        op.bulk_insert(
            addresses_table,
            [asdict(address) for address in addresses],
        )
    except Exception as err:
        logging.warning(f"Error with customer's addresses data insertion: {err}")
        raise


def downgrade():
    pass
