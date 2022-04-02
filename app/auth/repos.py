from typing import Optional

from fastapi import HTTPException
from sqlalchemy import update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.functions import now as sa_now
from starlette import status

from base.repo import BasePgRepo
from .errors import SessionNotFoundError, SessionExpiredError
from .models import WebUsers, SignupSession


class WebUserRepo(BasePgRepo):
    async def add(self, email: str, password: str) -> Optional[str]:
        web_users = WebUsers.__table__

        stmt = (
            insert(web_users)
            .values(
                email=email,
                password=password,
            )
            .returning(web_users.c.email)
        )

        try:
            cursor = await self.execute(stmt, debug=True)
        except IntegrityError:
            return None

        return cursor.scalar()

    async def update(self, email: str, **kwargs) -> Optional[WebUsers]:
        web_users = WebUsers.__table__

        stmt = (
            update(web_users)
            .values(**kwargs)
            .where(web_users.c.email == email)
            .returning(*web_users.c)
        )

        cursor = await self.execute(stmt)

        return WebUsers.from_cursor(cursor)

    async def upsert(self, email: str, password: str, **kwargs) -> WebUsers:
        web_users = WebUsers.__table__

        stmt = insert(web_users).values(email=email, password=password, **kwargs)

        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "password": password,
            },
        ).returning(*web_users.c)

        cursor = await self.execute(do_update_stmt)
        return WebUsers.from_cursor(cursor)

    async def get(self, email: str, only_active: bool = True) -> Optional[WebUsers]:
        users = WebUsers.__table__

        select_stmt = select(WebUsers)

        if only_active:
            stmt = select_stmt.where(
                and_(users.c.email == email, users.c.is_active.is_(True))
            )
        else:
            stmt = select_stmt.where(users.c.email == email)

        cursor = await self.execute(stmt, debug=True)
        return WebUsers.from_cursor(cursor)

    async def activate_account(self, email) -> str:
        web_user = await self.update(email=email, is_active=True)
        return web_user.email


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
            raise SessionExpiredError

        if session is None:
            raise SessionNotFoundError

        return session
