"""products data was added

Revision ID: df280473fa1c
Revises: 59ca10a9bd19
Create Date: 2022-04-10 18:21:35.170909

"""
import logging
from dataclasses import asdict
from pathlib import Path

from alembic import op
from sqlalchemy import Integer, Text, column, table

from scripts.faker.product_categories import (
    CATEGORIES_FILE,
    Category,
    PRODUCTS_FILE,
    Product,
)
from scripts.faker.rw import read

BASE_RETAILER_DIR = Path(__file__).resolve().parent.parent.parent

SCRIPTS_FILE = f"{BASE_RETAILER_DIR}/scripts/faker"


revision = "df280473fa1c"
down_revision = "59ca10a9bd19"
branch_labels = None
depends_on = None


def upgrade():
    pc_table = table(
        "product_categories",
        column("id", Integer),
        column("name", Text),
    )

    p_table = table(
        "products",
        column("id", Integer),
        column("name", Text),
        column("photo", Text),
        column("description", Text),
        column("category_id", Integer),
    )

    categories_raw, products_raw = read(f"{SCRIPTS_FILE}/{CATEGORIES_FILE}"), read(
        f"{SCRIPTS_FILE}/{PRODUCTS_FILE}"
    )

    categories = [Category(id=int(c["id"]), name=c["name"]) for c in categories_raw]
    products = [
        Product(
            name=p["name"],
            category_id=int(p["category_id"]),
            photo=p["photo"],
            description="",
        )
        for p in products_raw
    ]

    try:
        op.bulk_insert(
            pc_table,
            [asdict(c) for c in categories],
        )
        op.bulk_insert(
            p_table,
            [asdict(p) for p in products],
        )
    except Exception as err:
        logging.warning(f"Error with products' or categories' data insertion: {err}")
        raise


def downgrade():
    pass
