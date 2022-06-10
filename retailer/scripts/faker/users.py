import datetime
import string
from dataclasses import dataclass
from random import choice
from typing import Optional

from faker import Faker
from passlib.context import CryptContext

from scripts.faker.rw import write

COUNT = 1_000
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
    used_emails = set()

    result: list[User] = []
    for iteration in range(1, count + 1):
        if iteration % 500 == 0:
            print(f"{iteration} / {count}")

        email: str = f.email()

        while email in used_emails:
            email: str = f.email()

        used_emails.add(email)

        password = email.split("@")[0]

        if iteration < 10:
            password_hashed = pwd_context.hash(password)
        else:
            password_hashed = "".join(
                choice(string.ascii_uppercase + string.digits) for _ in range(30)
            )

        result.append(
            User(
                email=email,
                password=password_hashed,
                name=f.name(),
                birthday=f.date_of_birth(),
            )
        )

    return result


def generate(to_file: bool = False) -> list[User]:
    users = _generate_users(COUNT)

    if to_file:
        write(users, FILENAME_USERS)

    return users


if __name__ == "__main__":
    generate()
