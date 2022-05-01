"""user addresses table was added

Revision ID: 39f94d3d830d
Revises: 3dc8529d8689
Create Date: 2022-04-03 01:37:44.035674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "39f94d3d830d"
down_revision = "3dc8529d8689"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_addresses",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("city", sa.Text(), nullable=False),
        sa.Column("street", sa.Text(), nullable=False),
        sa.Column("house", sa.Text(), nullable=False),
        sa.Column("entrance", sa.Integer(), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=True),
        sa.Column("flat", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_addresses")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_addresses_user_id_users"),
        ),
    )
    op.create_index(
        op.f("ix_user_addresses_city"), "user_addresses", ["city"], unique=False
    )
    op.create_index(
        op.f("ix_user_addresses_street"),
        "user_addresses",
        ["street"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_addresses_street"), table_name="user_addresses")
    op.drop_index(op.f("ix_user_addresses_city"), table_name="user_addresses")
    op.drop_table("user_addresses")
    # ### end Alembic commands ###