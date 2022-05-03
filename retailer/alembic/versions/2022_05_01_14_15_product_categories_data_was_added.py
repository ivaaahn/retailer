"""product_categories data was added

Revision ID: c2f80473fa1c
Revises: 59ca10a9bd19
Create Date: 2022-04-10 18:09:35.170909

"""
import logging

from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import table, Integer, column, Text

revision = "c2f80473fa1c"
down_revision = "59ca10a9bd19"
branch_labels = None
depends_on = None


data = [
    {"name": "Кофе"},
    {"name": "Чай"},
    {"name": "Какао"},
]


def upgrade():
    pc_table = table(
        "product_categories",
        column("id", Integer),
        column("name", Text),
    )

    try:
        op.bulk_insert(pc_table, data)
    except Exception as err:
        logging.warning(f"Error with product_categories' data insertion: {err}")
        raise


def downgrade():
    pass