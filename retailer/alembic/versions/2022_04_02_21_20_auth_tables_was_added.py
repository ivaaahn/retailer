"""auth_tables_was_added

Revision ID: b6a744784764
Revises: 
Create Date: 2022-03-28 00:37:51.294370

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.

revision = "b6a744784764"
down_revision = None
branch_labels = None
depends_on = None

vals, name = ("client", "staff", "superuser"), "user_roles_enum"


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "is_active", sa.Boolean(), server_default=sa.text("false"), nullable=False
        ),
        sa.Column("name", sa.Text(), nullable=True),
        sa.Column("birthday", sa.Date(), nullable=True),
        sa.Column(
            "role",
            ENUM(*vals, name=name),
            nullable=False,
            server_default="client",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "signup_session",
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column("code", sa.String(length=8), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("attempts_left", sa.Integer(), server_default="3", nullable=False),
        sa.CheckConstraint(
            "attempts_left >= 0", name=op.f("ck_signup_session_attempts_left_check")
        ),
        sa.ForeignKeyConstraint(
            ["email"],
            ["users.email"],
            name=op.f("fk_signup_session_email_users"),
        ),
        sa.PrimaryKeyConstraint("email", name=op.f("pk_signup_session")),
    )

    permissions = (
        text("grant select, insert, update on users to defretailer;"),
        text("grant all on users to adretailer;"),
        text("grant select, insert, update on signup_session to defretailer"),
        text("grant all on signup_session to adretailer;"),
    )

    for perm in permissions:
        op.get_bind().execute(perm)


def downgrade():
    op.drop_table("signup_session")
    op.drop_table("users")
    psql_enum = ENUM(*vals, name=name)
    psql_enum.drop(op.get_bind())
