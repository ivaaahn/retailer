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


def downgrade():
    op.drop_constraint(
        constraint_name="ck_shop_products_qty_check",
        table_name="shop_products",
    )
