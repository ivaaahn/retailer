"""Add user_address to order table

Revision ID: 0d28cca50d97
Revises: 8g1856998bb3
Create Date: 2022-05-22 11:29:10.809828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0d28cca50d97"
down_revision = "8g1856998bb3"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("orders", sa.Column("address_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        op.f("fk_orders_address_id_user_addresses"),
        "orders",
        "user_addresses",
        ["address_id"],
        ["id"],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_orders_address_id_user_addresses"), "orders", type_="foreignkey"
    )
    op.drop_column("orders", "address_id")
    # ### end Alembic commands ###
