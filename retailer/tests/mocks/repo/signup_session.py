import pytest

from app.base.repo import BasePgRepo
from app.models.signup_sessions import SignupSessionModel
from app.services.auth.interfaces import ISignupSessionRepo
from store import PgAccessor
from store.pg.config import PgConfig


class SignupSessionRepoMock(ISignupSessionRepo, BasePgRepo):
    async def get(self, email: str) -> SignupSessionModel | None:
        pass

    async def upsert(self, email: str, code: str, **kwargs) -> SignupSessionModel:
        pass

    async def update_code(self, email: str, code: str) -> SignupSessionModel:
        pass

    async def update(self, email: str, **kwargs) -> SignupSessionModel | None:
        pass

    async def waste_attempt(self, email: str) -> SignupSessionModel:
        pass


@pytest.fixture
def signup_session_repo_mock() -> SignupSessionRepoMock:
    return SignupSessionRepoMock((PgAccessor(PgConfig())))
