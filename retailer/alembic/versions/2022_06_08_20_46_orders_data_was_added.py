"""Add orders data

Revision ID: 5be3768caf79
Revises: 4be3768caf79
Create Date: 2022-05-22 17:18:30.400804

"""

# revision identifiers, used by Alembic.

from retailer.app.models.orders import OrderReceiveKindEnum, OrderStatusEnum

revision = "5be3768caf79"
down_revision = "4be3768caf79"
branch_labels = None
depends_on = None

vals_rk, name_rk = (
    OrderReceiveKindEnum.takeaway.value,
    OrderReceiveKindEnum.delivery.value,
), "receive_kind_enum"
vals_s, name_s = (
    OrderStatusEnum.collecting.value,
    OrderStatusEnum.ready.value,
    OrderStatusEnum.delivering.value,
    OrderStatusEnum.delivered.value,
    OrderStatusEnum.cancelled.value,
    OrderStatusEnum.finished.value,
    OrderStatusEnum.error.value,
), "order_status_enum"


def upgrade():
    pass
    #
    # orders_table = table(
    #     "orders",
    #     column("id", Integer),
    #     column("user_id", Integer),
    #     column("shop_id", Integer),
    #     column("total_price", Float),
    #     column("receive_kind", ENUM(*vals_rk, name=name_rk)),
    #     column("status", ENUM(*vals_s, name=name_s)),
    #     column("address_id", Integer),
    #     column("created_at", DateTime),
    # )
    #
    # order_products_table = table(
    #     "order_products",
    #     column("id", Integer),
    #     column("product_id", Integer),
    #     column("order_id", Integer),
    #     column("qty", Integer),
    #     column("price", Float),
    # )
    #
    # orders, products = generate()
    #
    # try:
    #     op.bulk_insert(orders_table, orders)
    #     op.bulk_insert(order_products_table, products)
    #     op.get_bind().execute(
    #         text("SELECT SETVAL('orders_id_seq', COALESCE(MAX(id), 1) ) FROM orders;")
    #     )
    #     op.get_bind().execute(
    #         text(
    #             "SELECT SETVAL('order_products_id_seq', COALESCE(MAX(id), 1) ) FROM order_products;"
    #         )
    #     )
    # except Exception as err:
    #     logging.warning(f"Error with orders' data insertion: {err}")
    #     raise


def downgrade():
    pass
