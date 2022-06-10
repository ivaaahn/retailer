from dataclasses import dataclass

from faker import Faker

from scripts.faker.rw import write

ABC = "АБВ"
COUNT = 500
FILENAME_SHOPS = "data/shop.csv"


def _init_faker(seed: int) -> Faker:
    f = Faker("ru_RU")
    f.seed_instance(seed)
    return f


@dataclass
class Shop:
    address_id: int


def _generate_shop(count: int) -> list[Shop]:
    f = _init_faker(4321)

    result: list[Shop] = []
    for iteration in range(count):
        result.append(Shop(address_id=iteration + 1))

    return result


def generate(to_file: bool = False) -> list[Shop]:
    shop = _generate_shop(COUNT)

    if to_file:
        write(shop, FILENAME_SHOPS)

    return shop


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
