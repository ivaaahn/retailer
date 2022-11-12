import copy
from datetime import datetime

from app.dto.db.user import DBUserDTO
from app.models.users import UserRolesEnum
from tests.constants import (
    DEFAULT_DATETIME,
    DEFAULT_MAIL,
    DEFAULT_NAME,
    DEFAULT_PASSWORD_HASH,
)
from tests.builders.db.common import BaseBuilder


class DBUserBuilder(BaseBuilder):
    def __init__(self) -> None:
        self._id = 1
        self._email = DEFAULT_MAIL
        self._password = DEFAULT_PASSWORD_HASH
        self._created_at = DEFAULT_DATETIME
        self._is_active = False
        self._name = DEFAULT_NAME
        self._birthday = DEFAULT_DATETIME
        self._last_login = DEFAULT_DATETIME
        self._role = UserRolesEnum.client

    def but(self) -> "DBUserBuilder":
        return copy.deepcopy(self)

    def with_email(self, value: str) -> "DBUserBuilder":
        self._email = value
        return self

    def with_password(self, value: str) -> "DBUserBuilder":
        self._password = value
        return self

    def with_created_at(self, value: datetime) -> "DBUserBuilder":
        self._created_at = value
        return self

    def with_is_active(self, value: bool) -> "DBUserBuilder":
        self._is_active = value
        return self

    def with_name(self, value: str) -> "DBUserBuilder":
        self._name = value
        return self

    def with_birthday(self, value: datetime) -> "DBUserBuilder":
        self._birthday = value
        return self

    def with_last_login(self, value: datetime) -> "DBUserBuilder":
        self._last_login = value
        return self

    def with_role(self, value: UserRolesEnum) -> "DBUserBuilder":
        self._role = value
        return self

    def build(self) -> DBUserDTO:
        return DBUserDTO(
            id=self._id,
            email=self._email,
            password=self._password,
            created_at=self._created_at,
            is_active=self._is_active,
            name=self._name,
            birthday=self._birthday,
            last_login=self._last_login,
            role=self._role,
        )
