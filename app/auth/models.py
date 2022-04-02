from datetime import timedelta, datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    DateTime,
    Boolean,
    String,
    CheckConstraint,
    Index,
    ForeignKey,
)
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now

from app.base.models import BaseModel


# TODO добавить на email индекс
class WebUsers(BaseModel):
    __tablename__ = "web_users"

    id = Column(Integer, Identity(), primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=now())
    is_active = Column(Boolean, nullable=False, server_default=expression.false())


class SignupSession(BaseModel):
    ATTEMPTS = 3
    TIMEOUT = timedelta(minutes=1)

    __tablename__ = "signup_session"
    __table_args__ = (
        CheckConstraint("attempts_left >= 0", name="attempts_left_check"),
    )

    email = Column(Text, ForeignKey("web_users.email"), primary_key=True)
    code = Column(String(8), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=now())
    attempts_left = Column(Integer, server_default=str(ATTEMPTS), nullable=False)

    @property
    def send_code_timeout_expired(self) -> bool:
        return self.time_left.days < 0

    @property
    def is_attempts_exhausted(self) -> bool:
        return self.attempts_left <= 0

    @property
    def time_left(self) -> timedelta:
        return self.updated_at.replace(tzinfo=None) + self.TIMEOUT - datetime.utcnow()

    @property
    def seconds_left(self) -> int:
        return self.time_left.seconds
