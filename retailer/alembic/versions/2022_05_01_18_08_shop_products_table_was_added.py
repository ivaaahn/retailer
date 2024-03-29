"""shop_products table was added

Revision ID: 9ace568f3e17
Revises: df280473fa1c
Create Date: 2022-05-01 18:08:53.136077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import text

revision = "9ace568f3e17"
down_revision = "df280473fa1c"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shop_products",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("shop_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("qty", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name=op.f("fk_shop_products_product_id_products"),
        ),
        sa.ForeignKeyConstraint(
            ["shop_id"], ["shops.id"], name=op.f("fk_shop_products_shop_id_shops")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shop_products")),
    )

    # permissions = (
    #     text("grant select, update on shop_products to defretailer;"),
    #     text("grant all on shop_products to adretailer;"),
    # )
    #
    # for perm in permissions:
    #     op.get_bind().execute(perm)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("shop_products")
    # ### end Alembic commands ###
