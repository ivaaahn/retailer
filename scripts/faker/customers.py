from dataclasses import dataclass

from faker import Faker
from sqlalchemy import Date

from scripts.faker.rw import write

COUNT = 100
FILENAME_CUSTOMERS = "data/customers.csv"


def init_faker(seed: int) -> Faker:
    f_ = Faker("ru_RU")
    f_.seed_instance(seed)
    return f_


f = init_faker(1234)


@dataclass
class Customer:
    name: str
    user_id: int
    birthday: Date


def _generate_customers(count: int) -> list[Customer]:
    result: list[Customer] = []
    for iteration in range(count):
        result.append(
            Customer(
                name=f.name(),
                user_id=iteration + 1,
                birthday=f.date_of_birth(),
            )
        )

    return result


def generate(count: int, to_file: bool = False) -> list[Customer]:
    customers = _generate_customers(count)

    if to_file:
        write(customers, FILENAME_CUSTOMERS)

    return customers


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
