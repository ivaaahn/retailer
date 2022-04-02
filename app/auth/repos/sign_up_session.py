from typing import Optional

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.functions import now as sa_now

from base.errors import check_err, DBErrEnum
from base.repo import BasePgRepo
from ..errors import SessionNotFoundError, SignupSessionExpiredError, UserNotFoundError
from ..models import SignupSession


class SignupSessionRepo(BasePgRepo):
    async def get(self, email: str) -> Optional[SignupSession]:
        signup_session = SignupSession.__table__

        stmt = select(signup_session).where(signup_session.c.email == email)

        cursor = await self.execute(stmt, debug=True)
        return SignupSession.from_cursor(cursor)

    async def upsert(self, email: str, code: str, **kwargs) -> SignupSession:
        signup_session = SignupSession.__table__

        stmt = insert(signup_session).values(email=email, code=code, **kwargs)
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "updated_at": sa_now(),
                "attempts_left": SignupSession.ATTEMPTS,
            },
        ).returning(*signup_session.c)

        cursor = await self.execute(do_update_stmt)
        return SignupSession.from_cursor(cursor)

    async def update_code(self, email: str, code: str) -> SignupSession:
        signup_session = SignupSession.__table__

        stmt = (
            update(signup_session)
            .where(signup_session.c.email == email)
            .values(
                code=code,
                updated_at=sa_now(),
            )
            .returning(*signup_session.c)
        )

        cursor = await self.execute(stmt)
        return SignupSession.from_cursor(cursor)

    async def update(self, email: str, **kwargs) -> Optional[SignupSession]:
        signup_session = SignupSession.__table__

        stmt = (
            update(signup_session)
            .values(**kwargs)
            .where(signup_session.c.email == email)
            .returning(*signup_session.c)
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
