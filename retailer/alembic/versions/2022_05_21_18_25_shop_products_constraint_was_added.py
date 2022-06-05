"""shop_products constraint was added

Revision ID: 8g1856998bb3
Revises: bbcd1f6c9b84
Create Date: 2022-05-16 18:25:24.482739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8g1856998bb3"
down_revision = "bbcd1f6c9b84"
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        constraint_name="ck_shop_products_qty_check",
        table_name="shop_products",
        condition="qty >= 0",
    )
    op.create_index(
        index_name="shop_products_product_id_shop_id_idx",
        table_name="shop_products",
        columns=["product_id", "shop_id"],
        unique=True,
    )


def downgrade():
    op.drop_constraint(
        constraint_name="ck_shop_products_qty_check",
        table_name="shop_products",
    )
    op.drop_index(index_name="shop_products_product_id_shop_id_idx")
