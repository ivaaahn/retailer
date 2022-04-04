import datetime
from dataclasses import dataclass
from typing import Optional

from faker import Faker
from passlib.context import CryptContext

from scripts.faker.rw import write

COUNT = 100
FILENAME_USERS = "data/users.csv"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_faker(seed: int) -> Faker:
    f_ = Faker("ru_RU")
    f_.seed_instance(seed)
    return f_


f = init_faker(1234)


@dataclass
class User:
    email: str
    password: str
    name: Optional[str] = None
    birthday: Optional[datetime.date] = None
    is_active: bool = True


def _generate_users(count: int) -> list[User]:
    result: list[User] = []
    for iteration in range(1, count + 1):
        if iteration % 10 == 0:
            print(f"{iteration} / {count}")

        email: str = f.email()
        password = email.split("@")[0]
        password_hashed = pwd_context.hash(password)

        result.append(
            User(
                email=email,
                password=password_hashed,
                name=f.name(),
                birthday=f.date_of_birth(),
            )
        )

    return result


def generate(count: int, to_file: bool = False) -> list[User]:
    users = _generate_users(count)

    if to_file:
        write(users, FILENAME_USERS)

    return users


def main():
    generate(COUNT)


if __name__ == "__main__":
    main()
