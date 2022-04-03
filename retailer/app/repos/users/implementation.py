from functools import lru_cache
from typing import Optional

from sqlalchemy import update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from app.models import WebUsers
from base.repo import BasePgRepo


@lru_cache
class UsersRepo(BasePgRepo):
    async def update(self, email: str, **kwargs) -> Optional[WebUsers]:
        stmt = (
            update(WebUsers)
            .values(**kwargs)
            .where(WebUsers.c.email == email)
            .returning(*WebUsers.c)
        )

        cursor = await self._execute(stmt)

        return WebUsers.from_cursor(cursor)

    async def upsert(self, email: str, password: str, **kwargs) -> WebUsers:
        stmt = insert(WebUsers).values(email=email, password=password, **kwargs)

        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "password": password,
            },
        ).returning(*WebUsers.c)

        cursor = await self._execute(do_update_stmt)
        return WebUsers.from_cursor(cursor)

    async def get(self, email: str, only_active: bool = True) -> Optional[WebUsers]:
        select_stmt = select(WebUsers)

        if only_active:
            stmt = select_stmt.where(
                and_(WebUsers.c.email == email, WebUsers.c.is_active.is_(True))
            )
        else:
            stmt = select_stmt.where(WebUsers.c.email == email)

        cursor = await self._execute(stmt, debug=True)
        return WebUsers.from_cursor(cursor)
