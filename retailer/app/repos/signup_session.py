from typing import Optional

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.functions import now as sa_now

from app.api.auth.errors import SessionNotFoundError, SignupSessionExpiredError
from base.repo import BasePgRepo
from ..models import SignupSession


class SignupSessionRepo(BasePgRepo):
    @property
    def signup_session_t(self):
        return SignupSession.__table__

    async def get(self, email: str) -> Optional[SignupSession]:
        stmt = select(self.signup_session_t).where(
            self.signup_session_t.c.email == email
        )

        cursor = await self.execute(stmt, debug=True)
        return SignupSession.from_cursor(cursor)

    async def upsert(self, email: str, code: str, **kwargs) -> SignupSession:
        stmt = insert(self.signup_session_t).values(email=email, code=code, **kwargs)
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "updated_at": sa_now(),
                "attempts_left": SignupSession.ATTEMPTS,
            },
        ).returning(*self.signup_session_t.c)

        cursor = await self.execute(do_update_stmt)
        return SignupSession.from_cursor(cursor)

    async def update_code(self, email: str, code: str) -> SignupSession:
        stmt = (
            update(self.signup_session_t)
            .where(self.signup_session_t.c.email == email)
            .values(
                code=code,
                updated_at=sa_now(),
            )
            .returning(*self.signup_session_t.c)
        )

        cursor = await self.execute(stmt)
        return SignupSession.from_cursor(cursor)

    async def update(self, email: str, **kwargs) -> Optional[SignupSession]:
        stmt = (
            update(self.signup_session_t)
            .values(**kwargs)
            .where(self.signup_session_t.c.email == email)
            .returning(*self.signup_session_t.c)
        )

        cursor = await self.execute(stmt)
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
