"""customers and addresses tables was added

Revision ID: 49f94d3d830d
Revises: 9b55a88e1cd5
Create Date: 2022-04-03 01:37:44.035674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "49f94d3d830d"
down_revision = "9b55a88e1cd5"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "shops",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("address_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_shops")),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["shop_addresses.id"],
            name=op.f("fk_shops_address_id_shop_addresses"),
        ),
    )


def downgrade():
    op.drop_table("shops")
