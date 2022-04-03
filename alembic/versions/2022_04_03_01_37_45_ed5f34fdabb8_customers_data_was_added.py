"""customers data was added

Revision ID: ed5f34fdabb8
Revises: 39f94d3d830d
Create Date: 2022-04-03 17:47:15.305987

"""

import logging
from dataclasses import asdict

from alembic import op
from sqlalchemy import column, table, Integer, Text, Date

from scripts.faker.customers import Customer, generate

# revision identifiers, used by Alembic.
revision = "ed5f34fdabb8"
down_revision = "39f94d3d830d"
branch_labels = None
depends_on = None


def upgrade():
    customers_table = table(
        "customers",
        column("id", Integer),
        column("name", Text),
        column("user_id", Integer),
        column("birthday", Date),
    )

    customers: list[Customer] = generate(count=100)

    try:
        op.bulk_insert(
            customers_table,
            [asdict(customer) for customer in customers],
        )
    except Exception as err:
        logging.warning(f"Error with customers' data insertion: {err}")
        raise


def downgrade():
    pass
