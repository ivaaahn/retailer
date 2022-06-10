import random
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum

from faker import Faker
from passlib.context import CryptContext

COUNT = 250_000
USERS_COUNT = 1_000
SHOPS_COUNT = 500
PRODUCT_COUNT = 1_108
ADDRESSES_COUNT = 1_000

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_faker(seed: int) -> Faker:
    f_ = Faker("ru_RU")
    f_.seed_instance(seed)
    return f_


f = init_faker(1234)


class ReceiveKind(str, Enum):
    takeaway = "takeaway"
    delivery = "delivery"


class Status(str, Enum):
    collecting = "collecting"
    ready = "ready"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"
    finished = "finished"
    error = "error"


@dataclass
class OrderProduct:
    order_id: int
    product_id: int
    price: float
    qty: int


@dataclass
class Order:
    id: int
    user_id: int
    shop_id: int
    total_price: float
    receive_kind: ReceiveKind
    status: Status
    created_at: datetime
    address_id: int | None = None

    def as_dict(self) -> dict:
        res = asdict(self)
        res.pop("products")
        return res


def _generate_orders(count: int) -> tuple[list[dict], list[dict]]:
    orders: list[dict] = []
    products: list[dict] = []

    for iteration in range(1, count + 1):
        if iteration % 10000 == 0:
            print(f"{iteration} / {count}")

        if iteration % 10 == 0:
            recv_kind = ReceiveKind.delivery
            address_id = random.randint(1, ADDRESSES_COUNT)
        else:
            recv_kind = ReceiveKind.takeaway
            address_id = None

        order_products = [
            OrderProduct(
                order_id=iteration,
                product_id=random.randint(1, PRODUCT_COUNT),
                price=random.randint(100, 10000),
                qty=random.randint(1, 10),
            )
            for _ in range(random.randint(1, 10))
        ]
        products.extend([asdict(p) for p in order_products])

        order = Order(
            id=iteration,
            user_id=random.randint(1, USERS_COUNT),
            shop_id=random.randint(1, SHOPS_COUNT),
            total_price=sum([p.price for p in order_products]),
            receive_kind=recv_kind,
            status=random.choice(list(Status)),
            address_id=address_id,
            created_at=datetime(2020, 1, 1, 0, 0, 0, 0)
            + timedelta(
                hours=random.randint(1, 21120),
                minutes=random.randint(1, 59),
                seconds=random.randint(1, 59),
            ),
        )

        orders.append(asdict(order))

    return orders, products


def generate() -> tuple[list[dict], list[dict]]:
    return _generate_orders(COUNT)


if __name__ == "__main__":
    generate()
