import pytest

from app.services import ProfileService
from tests.mocks import UsersRepoMock


@pytest.fixture
def profile_service(users_repo_mock: UsersRepoMock) -> ProfileService:
    return ProfileService(users_repo_mock)
