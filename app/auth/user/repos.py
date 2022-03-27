from typing import Optional

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from auth.user.models import WebUsers
from base.repo import BasePgRepo


class AuthUserRepo(BasePgRepo):
    async def add(self, email: str, password: str) -> Optional[str]:
        table = WebUsers.__table__

        stmt = (
            insert(table)
            .values(
                email=email,
                password=password,
            )
            .returning(table.c.email)
        )

        try:
            cursor = await self.execute(stmt, debug=True)
        except IntegrityError:
            return None

        return cursor.scalar()

    async def get(self, email: str) -> Optional[WebUsers]:
        users = WebUsers.__table__

        stmt = select(WebUsers).where(users.c.email == email)

        cursor = await self.execute(stmt, debug=True)

        return cursor.first()
