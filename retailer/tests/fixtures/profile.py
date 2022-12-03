import pytest

from retailer.app.services import ProfileService
from retailer.tests.mocks import UsersRepoMock


@pytest.fixture
def profile_service(users_repo_mock: UsersRepoMock) -> ProfileService:
    return ProfileService(users_repo_mock)
