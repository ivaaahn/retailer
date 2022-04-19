"""products data was added

Revision ID: c2f80473fa1c
Revises: 1551d7b903c9
Create Date: 2022-04-10 18:09:35.170909

"""
import logging

from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy import table, Integer, column, Text

revision = "df280473fa1c"
down_revision = "c2f80473fa1c"
branch_labels = None
depends_on = None


data = [
    {
        "name": "Флэт Уайт",
        "category_id": 1,
    },
    {
        "name": "Американо",
        "category_id": 1,
    },
    {
        "name": "Капучино",
        "category_id": 1,
    },
    {
        "name": "Латте",
        "category_id": 1,
    },
    {
        "name": "Раф",
        "category_id": 1,
    },
    {
        "name": "Мокко",
        "category_id": 1,
    },
    {
        "name": "Кармелатте",
        "category_id": 1,
    },
    {
        "name": "Черный",
        "category_id": 2,
    },
    {
        "name": "Зеленый",
        "category_id": 2,
    },
    {
        "name": "Какао",
        "category_id": 3,
    },
    {
        "name": "Какао со взбитыми сливками",
        "category_id": 3,
    },
]


def upgrade():
    p_table = table(
        "products",
        column("id", Integer),
        column("name", Text),
        column("photo", Text),
        column("description", Text),
        column("category_id", Integer),
    )

    try:
        op.bulk_insert(p_table, data)
    except Exception as err:
        logging.warning(f"Error with products' data insertion: {err}")
        raise


def downgrade():
    pass
