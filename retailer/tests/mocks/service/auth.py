from datetime import timedelta
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from app.services.auth.config import AuthConfig
from tests.builders.db.user import DBUserBuilder
from tests.constants import (
    DEFAULT_CODE,
    DEFAULT_DATETIME,
    DEFAULT_JWT_ACCESS_TOKEN,
    DEFAULT_PASSWORD_HASH,
)


@pytest.fixture
def auth_config() -> AuthConfig:
    return AuthConfig()


@pytest.fixture
def jwt_encode_mocked(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        target="jose.jwt.encode",
        return_value=DEFAULT_JWT_ACCESS_TOKEN,
    )


@pytest.fixture
def jwt_encode_call_args_default(
    auth_config: AuthConfig, default_user_to_build: DBUserBuilder
) -> dict:
    return dict(
        claims={
            "sub": default_user_to_build.build().email,
            "exp": DEFAULT_DATETIME
            + timedelta(minutes=auth_config.access_token_exp_minutes),
        },
        key=auth_config.secret,
        algorithm=auth_config.alg,
    )


@pytest.fixture
def auth_get_password_hash_mocked(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "app.services.auth.service.pwd_context.hash",
        return_value=DEFAULT_PASSWORD_HASH,
    )


@pytest.fixture
def auth_verify_pass_mocked(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        "app.services.auth.service.pwd_context.verify",
        return_value=True,
    )


@pytest.fixture
def patch_auth_service(
    mocker: MockerFixture,
    auth_get_password_hash_mocked: MagicMock,
    auth_verify_pass_mocked: MagicMock,
) -> None:
    mocker.patch(
        "app.services.AuthService._generate_code",
        return_value=DEFAULT_CODE,
    )
