"""shop_addresses table was added

Revision ID: 9b55a88e1cd5
Revises: 39f94d3d830d
Create Date: 2022-05-01 14:02:52.627892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b55a88e1cd5"
down_revision = "39f94d3d830d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shop_addresses",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("city", sa.Text(), nullable=False),
        sa.Column("street", sa.Text(), nullable=False),
        sa.Column("house", sa.Text(), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shop_addresses")),
    )
    op.create_index(
        op.f("ix_shop_addresses_city"), "shop_addresses", ["city"], unique=False
    )
    op.create_index(
        op.f("ix_shop_addresses_street"), "shop_addresses", ["street"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_shop_addresses_street"), table_name="shop_addresses")
    op.drop_index(op.f("ix_shop_addresses_city"), table_name="shop_addresses")
    op.drop_table("shop_addresses")
