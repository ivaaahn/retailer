import copy
from datetime import datetime

from app.dto.db.signup_session import DBSignupSessionDTO
from tests.builders.db.common import BaseBuilder
from tests.constants import (
    DEFAULT_ATTEMPTS_LEFT,
    DEFAULT_CODE,
    DEFAULT_DATETIME,
    DEFAULT_MAIL,
)


class DBSignupSessionBuilder(BaseBuilder):
    def __init__(self) -> None:
        self._email = DEFAULT_MAIL
        self._code = DEFAULT_CODE
        self._updated_at = DEFAULT_DATETIME
        self._attempts_left = DEFAULT_ATTEMPTS_LEFT

    def but(self) -> "DBSignupSessionBuilder":
        return copy.deepcopy(self)

    def with_email(self, value: str) -> "DBSignupSessionBuilder":
        self._email = value
        return self

    def with_code(self, value: str) -> "DBSignupSessionBuilder":
        self._code = value
        return self

    def with_updated_at(self, value: datetime) -> "DBSignupSessionBuilder":
        self._updated_at = value
        return self

    def with_attempts_at(self, value: int) -> "DBSignupSessionBuilder":
        self._attempts_left = value
        return self

    def build(self) -> DBSignupSessionDTO:
        return DBSignupSessionDTO(
            email=self._email,
            code=self._code,
            updated_at=self._updated_at,
            attempts_left=self._attempts_left,
        )
