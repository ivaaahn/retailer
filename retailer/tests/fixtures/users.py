import pytest
from pydantic import EmailStr

from app.dto.api.user import UserRespDTO
from app.services import AuthService
from app.services.auth.config import AuthConfig
from tests.builders.db.signup_session import DBSignupSessionBuilder
from tests.builders.db.user import DBUserBuilder
from tests.mocks import RMQInteractionRepoMock, SignupSessionRepoMock, UsersRepoMock


@pytest.fixture
def default_user_to_build() -> DBUserBuilder:
    return DBUserBuilder()


@pytest.fixture
def default_active_user_to_build(default_user_to_build: DBUserBuilder) -> DBUserBuilder:
    return default_user_to_build.but().with_is_active(True)


@pytest.fixture
def default_active_user_api(default_active_user_to_build: DBUserBuilder) -> UserRespDTO:
    user = default_active_user_to_build.build()
    return UserRespDTO(
        id=1,
        email=EmailStr(user.email),
        created_at=user.created_at,
        is_active=user.is_active,
        name=user.name,
        birthday=user.birthday,
        role=user.role,
    )


@pytest.fixture
def default_signup_session_to_build() -> DBSignupSessionBuilder:
    return DBSignupSessionBuilder()


@pytest.fixture
def default_attempt_wasted_signup_session_to_build(
    default_signup_session_to_build: DBSignupSessionBuilder,
) -> DBSignupSessionBuilder:
    return default_signup_session_to_build.but().with_attempts_at(2)


@pytest.fixture
def auth_service(
    users_repo_mock: UsersRepoMock,
    signup_session_repo_mock: SignupSessionRepoMock,
    rmq_interaction_repo_mock: RMQInteractionRepoMock,
    auth_config: AuthConfig,
) -> AuthService:
    return AuthService(
        users_repo=users_repo_mock,
        signup_session_repo=signup_session_repo_mock,
        rmq_interact_repo=rmq_interaction_repo_mock,
        config=auth_config,
    )
