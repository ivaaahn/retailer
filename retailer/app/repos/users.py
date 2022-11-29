from functools import lru_cache

from app.base.repo import BasePgRepo
from app.delivery.profile.errors import AddressesNotFoundError
from app.dto.db.profile import DBAddressDTO, DBAddressListDTO
from app.models.user_addresses import UserAddressModel
from app.models.users import UserModel
from sqlalchemy import and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select


@lru_cache
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

        return DBAddressListDTO(
            [
                DBAddressDTO(
                    id=addr.id,
                    city=addr.city,
                    street=addr.street,
                    house=addr.house,
                    entrance=addr.entrance,
                    floor=addr.floor,
                    flat=addr.flat,
                )
                for addr in cursor
            ]
        )

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

    async def update(self, email: str, **kwargs) -> UserModel | None:
        stmt = (
            update(UserModel)
            .values(**kwargs)
            .where(UserModel.__table__.c.email == email)
            .returning(*UserModel.__table__.c)
        )

        cursor = await self._execute(stmt)

        return UserModel.from_cursor(cursor)

    async def upsert(self, email: str, password: str, **kwargs) -> UserModel:
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
        return UserModel.from_cursor(cursor)

    async def get(
        self, email: str, only_active: bool = True
    ) -> UserModel | None:
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
        return UserModel.from_cursor(cursor)
