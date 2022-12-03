from sqlalchemy import and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from retailer.app.base.repo import BasePgRepo
from retailer.app.delivery.profile.errors import AddressesNotFoundError
from retailer.app.dto.db.profile import DBAddressListDTO
from retailer.app.dto.db.user import DBUserDTO
from retailer.app.models.user_addresses import UserAddressModel
from retailer.app.models.users import UserModel

__all__ = ("UsersRepo",)


class UsersRepo(BasePgRepo):
    async def get_addresses_list(self, user_id: int) -> DBAddressListDTO:
        user_addr = UserAddressModel.__table__

        stmt = (
            select(user_addr)
            .where(user_addr.c.user_id == user_id)
            .select_from(user_addr)
        )

        cursor = await self._execute(stmt)
        if not cursor:
            raise AddressesNotFoundError(user_id)

        return DBAddressListDTO.from_db(cursor)

    async def add_address(
        self,
        user_id: int,
        city: str,
        street: str,
        house: str,
        entrance: int,
        floor: int | None,
        flat: str | None,
    ) -> int:
        user_addr_t = UserAddressModel.__table__

        stmt = insert(user_addr_t).values(
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

    async def update(self, email: str, **kwargs) -> DBUserDTO | None:
        stmt = (
            update(UserModel)
            .values(**kwargs)
            .where(UserModel.__table__.c.email == email)
            .returning(*UserModel.__table__.c)
        )

        cursor = await self._execute(stmt)
        return DBUserDTO.from_db(cursor.first())

    async def upsert(self, email: str, password: str, **kwargs) -> DBUserDTO:
        stmt = insert(UserModel).values(
            email=email, password=password, **kwargs
        )

        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "password": password,
            },
        ).returning(*UserModel.__table__.c)

        cursor = await self._execute(do_update_stmt)
        return DBUserDTO.from_db(cursor.first())

    async def get(
        self, email: str, only_active: bool = True
    ) -> DBUserDTO | None:
        select_stmt = select(UserModel)

        if not only_active:
            stmt = select_stmt.where(UserModel.__table__.c.email == email)
        else:
            stmt = select_stmt.where(
                and_(
                    UserModel.__table__.c.email == email,
                    UserModel.__table__.c.is_active.is_(True),
                )
            )

        cursor = await self._execute(stmt)
        return DBUserDTO.from_db(cursor.first())
