import pytest

from app.base.repo import BasePgRepo
from app.dto.db.profile import DBAddressListDTO
from app.models.users import UserModel
from app.services.auth.interfaces import IUserRepo
from store import PgAccessor
from store.pg.config import PgConfig


class UsersRepoMock(IUserRepo, BasePgRepo):
    async def get(self, email: str, only_active: bool = True) -> UserModel | None:
        pass

    async def upsert(self, email: str, password: str, **kwargs) -> UserModel:
        pass

    async def update(self, email: str, **kwargs) -> UserModel | None:
        pass

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
        pass

    async def get_addresses_list(self, user_id: int) -> DBAddressListDTO:
        pass


@pytest.fixture
def users_repo_mock() -> UsersRepoMock:
    return UsersRepoMock(PgAccessor(PgConfig()))
