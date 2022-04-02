import random
from dataclasses import dataclass
from typing import Optional

from faker import Faker

from scripts.faker.rw import write

COUNT = 100
FILENAME_CUSTOMERS = "data/customer_addresses.csv"
FILENAME_SHOPS = "data/shop_addresses.csv"

HOUSES = [str(h) for h in range(1, 100)]
ENTRANCES = [_ for _ in range(1, 10)]
FLOORS = [f for f in range(1, 32)]


def init_faker() -> Faker:
    return Faker("ru_RU")


@dataclass
class Address:
    city: str
    street: str
    house: str


@dataclass
class ShopAddress(Address):
    building: Optional[str] = None
    floor: Optional[int] = None


@dataclass
class CustomerAddress(Address):
    entrance: int
    floor: Optional[int] = None
    flat: Optional[str] = None


def _generate_shop_addresses(count: int) -> list[ShopAddress]:
    f = init_faker()

    result: list[ShopAddress] = []
    for iteration in range(count):
        building, floor = None, None
        if iteration % 35 == 0:
            building = random.choice(HOUSES)
        if iteration % 20 == 0:
            floor = random.choice(FLOORS)

        result.append(
            ShopAddress(
                city=f.city(),
                street=f.street_name(),
                house=random.choice(HOUSES),
                building=building,
                floor=floor,
            )
        )

    return result


def _generate_customer_addresses(count: int) -> list[CustomerAddress]:
    f = init_faker()

    result: list[CustomerAddress] = []
    for iteration in range(count):
        entrance = random.choice(ENTRANCES)

        floor, flat = None, None
        if iteration % 10:
            floor = random.choice(FLOORS)
            from_ = entrance * floor * 5
            to_ = (entrance + 1) * floor * 10
            flat = random.choice([_ for _ in range(from_, to_)])

        result.append(
            CustomerAddress(
                city=f.city(),
                street=f.street_name(),
                house=random.choice(HOUSES),
                entrance=entrance,
                floor=floor,
                flat=flat,
            )
        )

    return result


def generate(count: int) -> tuple[list[ShopAddress], list[CustomerAddress]]:
    customers = _generate_customer_addresses(count)
    write(customers, FILENAME_CUSTOMERS)

    shops = _generate_shop_addresses(count)
    write(shops, FILENAME_SHOPS)

    return shops, customers


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
