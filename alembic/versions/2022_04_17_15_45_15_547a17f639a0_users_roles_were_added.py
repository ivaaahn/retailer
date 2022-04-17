"""Users roles were added

Revision ID: 547a17f639a0
Revises: df280473fa1c
Create Date: 2022-04-17 15:45:15.023886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.dialects import postgresql

revision = "547a17f639a0"
down_revision = "df280473fa1c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    user_roles_enum = postgresql.ENUM(
        "regular", "staff", "superuser", name="user_roles_enum"
    )
    user_roles_enum.create(op.get_bind())

    op.create_table(
        "shop_managers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("shop_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["shop_id"], ["shops.id"], name=op.f("fk_shop_managers_shop_id_shops")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_shop_managers_user_id_users")
        ),
        sa.PrimaryKeyConstraint("user_id", "shop_id", name=op.f("pk_shop_managers")),
    )
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("regular", "staff", "superuser", name="user_roles_enum"),
            server_default="regular",
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "role")
    op.drop_table("shop_managers")
    user_roles_enum = postgresql.ENUM(
        "regular", "staff", "superuser", name="user_roles_enum"
    )
    user_roles_enum.drop(op.get_bind())

    # ### end Alembic commands ###