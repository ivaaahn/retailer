from functools import lru_cache
from typing import Optional

from sqlalchemy import update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from app.models import Users
from base.repo import BasePgRepo
from .interface import IUsersRepo


@lru_cache
class UsersRepo(IUsersRepo, BasePgRepo):
    async def update(self, email: str, **kwargs) -> Optional[Users]:
        stmt = (
            update(Users)
            .values(**kwargs)
            .where(Users.__table__.c.email == email)
            .returning(*Users.__table__.c)
        )

        cursor = await self._execute(stmt, debug=True)

        return Users.from_cursor(cursor)

    async def upsert(self, email: str, password: str, **kwargs) -> Users:
        stmt = insert(Users).values(email=email, password=password, **kwargs)

        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "password": password,
            },
        ).returning(*Users.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return Users.from_cursor(cursor)

    async def get(self, email: str, only_active: bool = True) -> Optional[Users]:
        select_stmt = select(Users)

        if only_active:
            stmt = select_stmt.where(
                and_(
                    Users.__table__.c.email == email,
                    Users.__table__.c.is_active.is_(True),
                )
            )
        else:
            stmt = select_stmt.where(Users.__table__.c.email == email)

        cursor = await self._execute(stmt, debug=True)
        return Users.from_cursor(cursor)
