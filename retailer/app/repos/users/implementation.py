from functools import lru_cache
from typing import Optional

from sqlalchemy import update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from app.models import WebUsers
from base.repo import BasePgRepo
from .interface import IUsersRepo


@lru_cache
class UsersRepo(IUsersRepo, BasePgRepo):
    async def update(self, email: str, **kwargs) -> Optional[WebUsers]:
        stmt = (
            update(WebUsers)
            .values(**kwargs)
            .where(WebUsers.__table__.c.email == email)
            .returning(*WebUsers.__table__.c)
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
        ).returning(*WebUsers.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return WebUsers.from_cursor(cursor)

    async def get(self, email: str, only_active: bool = True) -> Optional[WebUsers]:
        select_stmt = select(WebUsers)

        if only_active:
            stmt = select_stmt.where(
                and_(
                    WebUsers.__table__.c.email == email,
                    WebUsers.__table__.c.is_active.is_(True),
                )
            )
        else:
            stmt = select_stmt.where(WebUsers.__table__.c.email == email)

        cursor = await self._execute(stmt, debug=True)
        return WebUsers.from_cursor(cursor)
