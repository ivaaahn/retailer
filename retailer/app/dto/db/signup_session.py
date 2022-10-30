from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from app.models.signup_sessions import SignupSessionModel


@dataclass
class DBSignupSessionDTO:
    email: str
    code: str
    updated_at: datetime
    attempts_left: int

    @classmethod
    def from_db(cls, db: Mapping | None) -> Optional["DBSignupSessionDTO"]:
        return cls(**db) if db else None

    @property
    def send_code_timeout_expired(self) -> bool:
        return self.time_left.days < 0

    @property
    def is_attempts_exhausted(self) -> bool:
        return self.attempts_left <= 0

    @property
    def time_left(self) -> timedelta:
        return (
            self.updated_at.replace(tzinfo=None)
            + SignupSessionModel.TIMEOUT
            - datetime.utcnow()
        )

    @property
    def seconds_left(self) -> int:
        return self.time_left.seconds
