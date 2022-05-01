import random
from dataclasses import dataclass
from typing import Optional

from faker import Faker

from scripts.faker.rw import write

ABC = "АБВ"
COUNT = 10
FILENAME_SHOP_ADDRESSES = "data/shop_addresses.csv"


def get_random_floor() -> int:
    return random.randint(1, 6)


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
class ShopAddress:
    city: str
    street: str
    house: str
    floor: Optional[int] = None


def _generate_shop_addresses(count: int) -> list[ShopAddress]:
    f = _init_faker(1234)

    result: list[ShopAddress] = []
    for iteration in range(count):
        floor = None
        if iteration % 20 == 0:
            floor = get_random_floor()

        result.append(
            ShopAddress(
                city=f.city(),
                street=f.street_name(),
                house=get_random_house(),
                floor=floor,
            )
        )

    return result


def generate(to_file: bool = False) -> list[ShopAddress]:
    shop_addresses = _generate_shop_addresses(COUNT)

    if to_file:
        write(shop_addresses, FILENAME_SHOP_ADDRESSES)

    return shop_addresses


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
