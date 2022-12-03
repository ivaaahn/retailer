import pytest

from retailer.app.base.repo import BasePgRepo
from retailer.app.dto.db.profile import DBAddressListDTO
from retailer.app.models.users import UserModel
from retailer.app.services.auth.interfaces import IUserRepo
from retailer.store import PgAccessor
from retailer.store.pg.config import PgConfig


class UsersRepoMock(IUserRepo, BasePgRepo):
    async def get(
        self, email: str, only_active: bool = True
    ) -> UserModel | None:
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
