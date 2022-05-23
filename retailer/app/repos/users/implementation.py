from functools import lru_cache
from typing import Optional

from sqlalchemy import update, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from app.base.repo import BasePgRepo
from app.models.users import UserModel
from .interface import IUsersRepo
from app.models.user_addresses import UserAddressModel


@lru_cache
class UsersRepo(IUsersRepo, BasePgRepo):
    async def add(
            self,
            user_id: int,
            city: str,
            street: str,
            house: str,
            entrance: int,
            floor: Optional[int],
            flat: Optional[str],
    ) -> int:
        user_addr = UserAddressModel.__table__

        stmt = insert(user_addr).values(
            user_id=user_id,
            city=city,
            street=street,
            house=house,
            entrance=entrance,
            floor=floor,
            flat=flat,
        )

        addr_id = await self.execute_with_pk(stmt)

        return addr_id

    async def update(self, email: str, **kwargs) -> Optional[UserModel]:
        stmt = (
            update(UserModel)
            .values(**kwargs)
            .where(UserModel.__table__.c.email == email)
            .returning(*UserModel.__table__.c)
        )

        cursor = await self._execute(stmt)

        return UserModel.from_cursor(cursor)

    async def upsert(self, email: str, password: str, **kwargs) -> UserModel:
        stmt = insert(UserModel).values(email=email, password=password, **kwargs)

        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "password": password,
            },
        ).returning(*UserModel.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return UserModel.from_cursor(cursor)

    async def get(self, email: str, only_active: bool = True) -> Optional[UserModel]:
        select_stmt = select(UserModel)

        if only_active:
            stmt = select_stmt.where(
                and_(
                    UserModel.__table__.c.email == email,
                    UserModel.__table__.c.is_active.is_(True),
                )
            )
        else:
            stmt = select_stmt.where(UserModel.__table__.c.email == email)

        cursor = await self._execute(stmt)
        return UserModel.from_cursor(cursor)
