"""Fix qty nullable in shop_products table

Revision ID: 4be3768caf79
Revises: 0d28cca50d97
Create Date: 2022-05-22 17:18:30.400804

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4be3768caf79"
down_revision = "0d28cca50d97"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("shop_products", "qty", existing_type=sa.INTEGER(), nullable=False)


def downgrade():
    op.alter_column("shop_products", "qty", existing_type=sa.INTEGER(), nullable=True)
