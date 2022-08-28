import random
from dataclasses import dataclass
from typing import Optional

from faker import Faker

from scripts.faker.rw import write

ABC = "АБВ"
COUNT = 1_000
FILENAME_CUSTOMERS = "data/customer_addresses.csv"


def get_random_floor() -> int:
    return random.randint(1, 32)


def get_random_entrance() -> int:
    return random.randint(1, 10)


def get_random_house() -> str:
    a = str(random.randint(1, 100))
    b = str(random.randint(1, 100))
    c = random.choice(ABC)

    population = (
        f"{a}",
        f"{a}{c}",
        f"{a}/{b}",
        f"{a}/{b}{c}",
    )

    weights = (4, 3, 2, 1)

    return random.choices(population, weights, k=1)[0]


def _init_faker(seed: int) -> Faker:
    f = Faker("ru_RU")
    f.seed_instance(seed)
    return f


@dataclass
class UserAddress:
    user_id: int
    city: str
    street: str
    house: str
    entrance: int
    floor: int | None = None
    flat: str | None = None


def _generate_customer_addresses(count: int) -> list[UserAddress]:
    f = _init_faker(4321)

    result: list[UserAddress] = []
    for iteration in range(count):
        entrance = get_random_entrance()

        floor, flat = None, None
        if iteration % 10:
            floor = get_random_floor()
            from_ = entrance * floor * 5
            to_ = (entrance + 1) * floor * 10
            flat = str(random.randint(from_, to_))
        result.append(
            UserAddress(
                user_id=iteration + 1,
                city=f.city(),
                street=f.street_name(),
                house=get_random_house(),
                entrance=entrance,
                floor=floor,
                flat=flat,
            )
        )

    return result


def generate(to_file: bool = False) -> list[UserAddress]:
    customer_addresses = _generate_customer_addresses(COUNT)

    if to_file:
        write(customer_addresses, FILENAME_CUSTOMERS)

    return customer_addresses


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
