"""order_products table was added

Revision ID: bbcd1f6c9b84
Revises: 7g1856998bb3
Create Date: 2022-05-16 18:25:24.482739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = "bbcd1f6c9b84"
down_revision = "7g1856998bb3"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "order_products",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], name=op.f("fk_order_products_order_id_orders")
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_order_products_product_id_products"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_order_products")),
    )

    permissions = (
        text("grant select, insert on orders to defretailer;"),
        text("grant all on orders to adretailer;"),
    )

    for perm in permissions:
        op.get_bind().execute(perm)


def downgrade():
    op.drop_table("order_products")
