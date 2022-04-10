from functools import lru_cache
from typing import Optional

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.functions import now as sa_now

from app.api.auth.errors import SessionNotFoundError, SignupSessionExpiredError
from app.base.repo import BasePgRepo
from app.models import SignupSession
from .interface import ISignupSessionRepo


@lru_cache
class SignupSessionRepo(ISignupSessionRepo, BasePgRepo):
    async def get(self, email: str) -> Optional[SignupSession]:
        stmt = select(SignupSession).where(SignupSession.__table__.c.email == email)

        cursor = await self._execute(stmt)
        return SignupSession.from_cursor(cursor)

    async def upsert(self, email: str, code: str, **kwargs) -> SignupSession:
        stmt = insert(SignupSession).values(email=email, code=code, **kwargs)
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "updated_at": sa_now(),
                "attempts_left": SignupSession.ATTEMPTS,
            },
        ).returning(*SignupSession.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return SignupSession.from_cursor(cursor)

    async def update_code(self, email: str, code: str) -> SignupSession:
        stmt = (
            update(SignupSession)
            .where(SignupSession.__table__.c.email == email)
            .values(
                code=code,
                updated_at=sa_now(),
            )
            .returning(*SignupSession.__table__.c)
        )

        cursor = await self._execute(stmt)
        return SignupSession.from_cursor(cursor)

    async def update(self, email: str, **kwargs) -> Optional[SignupSession]:
        stmt = (
            update(SignupSession)
            .values(**kwargs)
            .where(SignupSession.__table__.c.email == email)
            .returning(*SignupSession.__table__.c)
        )

        cursor = await self._execute(stmt)
        return SignupSession.from_cursor(cursor)

    async def waste_attempt(self, email: str) -> SignupSession:
        try:
            session = await self.update(
                email=email,
                attempts_left=SignupSession.attempts_left - 1,
            )
        except IntegrityError:
            raise SignupSessionExpiredError

        if session is None:
            raise SessionNotFoundError

        return session
