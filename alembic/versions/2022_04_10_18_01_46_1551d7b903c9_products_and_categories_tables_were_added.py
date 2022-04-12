"""products and categories tables were added

Revision ID: 1551d7b903c9
Revises: 6396f15cadeb
Create Date: 2022-04-10 18:01:46.932822

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "1551d7b903c9"
down_revision = "6396f15cadeb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_categories",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_product_categories")),
    )
    op.create_index(
        op.f("ix_product_categories_name"),
        "product_categories",
        [sa.text("lower(name)")],
        unique=True,
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("photo", sa.Text(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["product_categories.id"],
            name=op.f("fk_products_category_id_product_categories"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_products")),
    )
    op.create_index(
        op.f("ix_products_name"), "products", [sa.text("lower(name)")], unique=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_product_categories_name"), table_name="product_categories")
    op.drop_table("product_categories")
    # ### end Alembic commands ###
