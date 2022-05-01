from functools import lru_cache
from typing import Optional

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.functions import now as sa_now

from app.base.repo import BasePgRepo
from app.delivery.auth.errors import SessionNotFoundError, SignupSessionExpiredError
from app.models.signup_session import SignupSessionModel
from .interface import ISignupSessionRepo


@lru_cache
class SignupSessionRepo(ISignupSessionRepo, BasePgRepo):
    async def get(self, email: str) -> Optional[SignupSessionModel]:
        stmt = select(SignupSessionModel).where(
            SignupSessionModel.__table__.c.email == email
        )

        cursor = await self._execute(stmt)
        return SignupSessionModel.from_cursor(cursor)

    async def upsert(self, email: str, code: str, **kwargs) -> SignupSessionModel:
        stmt = insert(SignupSessionModel).values(email=email, code=code, **kwargs)
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "updated_at": sa_now(),
                "attempts_left": SignupSessionModel.ATTEMPTS,
                "code": code,
            },
        ).returning(*SignupSessionModel.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return SignupSessionModel.from_cursor(cursor)

    async def update_code(self, email: str, code: str) -> SignupSessionModel:
        stmt = (
            update(SignupSessionModel)
            .where(SignupSessionModel.__table__.c.email == email)
            .values(
                code=code,
                updated_at=sa_now(),
            )
            .returning(*SignupSessionModel.__table__.c)
        )

        cursor = await self._execute(stmt)
        return SignupSessionModel.from_cursor(cursor)

    async def update(self, email: str, **kwargs) -> Optional[SignupSessionModel]:
        stmt = (
            update(SignupSessionModel)
            .values(**kwargs)
            .where(SignupSessionModel.__table__.c.email == email)
            .returning(*SignupSessionModel.__table__.c)
        )

        cursor = await self._execute(stmt)
        return SignupSessionModel.from_cursor(cursor)

    async def waste_attempt(self, email: str) -> SignupSessionModel:
        try:
            session = await self.update(
                email=email,
                attempts_left=SignupSessionModel.attempts_left - 1,
            )
        except IntegrityError:
            raise SignupSessionExpiredError

        if session is None:
            raise SessionNotFoundError

        return session
