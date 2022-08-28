"""Add stats function

Revision ID: 6be3768caf79
Revises: 5be3768caf79
Create Date: 2022-05-22 17:18:30.400804

"""
import logging
from dataclasses import asdict

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import DateTime, Float, Integer, String, column, table, text
from sqlalchemy.dialects.postgresql import ENUM

from app.models.orders import OrderReceiveKindEnum, OrderStatusEnum
from scripts.faker.orders import Order, generate

revision = "6be3768caf79"
down_revision = "5be3768caf79"
branch_labels = None
depends_on = None

SQL = """
create or replace function order_stats(in count int, in date_from date, in date_to date)
    returns table
            (
                shop_id             int,
                shop_orders_qty     bigint,
                shop_total_profit   float,
                shop_address        text,
                client_name         text,
                client_orders_qty   bigint,
                client_spend        float
            )
as
$$
select o.shop_id                                              as shop_id,
       count(o.id)                                            as shop_orders_qty,
       sum(o.total_price)                                     as shop_total_profit,
       concat(sa.city || ' ' || sa.street || ' ' || sa.house) as shop_address,
       bc.name                                                as client_name,
       bc.sum_count                                           as client_orders_qty,
       bc.sum_total                                           as client_spend
from orders o
         join shops s on o.shop_id = s.id
         join shop_addresses sa on s.address_id = sa.id
         join (select distinct on (shop_id) shop_id,
                                            user_id,
                                            u.name,
                                            sum(total_price) over (partition by shop_id, user_id) as sum_total,
                                            count(*) over (partition by shop_id, user_id)         as sum_count
               from orders o2
                        join users u on o2.user_id = u.id
               where o2.created_at between date_from and date_to
               order by shop_id, sum_total desc, user_id) as bc on bc.shop_id = o.shop_id
where o.created_at between date_from and date_to
group by o.shop_id, sa.city, sa.street, sa.house, bc.sum_count, bc.name, bc.sum_total
order by shop_total_profit desc
limit count;
$$ language SQL;
"""


def upgrade():
    try:
        op.get_bind().execute(text(SQL))
    except Exception as err:
        logging.warning(f"Error with orders' data insertion: {err}")
        raise


def downgrade():
    pass
