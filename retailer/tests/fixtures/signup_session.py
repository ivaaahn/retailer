from collections.abc import Callable
from datetime import datetime, timedelta

import pytest
from jose import jwt

from retailer.app.services.auth.config import AuthConfig
from retailer.tests.builders.db.signup_session import DBSignupSessionBuilder
from retailer.tests.constants import DEFAULT_DATETIME, DEFAULT_EMAIL


@pytest.fixture
def default_signup_session_to_build() -> DBSignupSessionBuilder:
    return DBSignupSessionBuilder()


@pytest.fixture
def access_token_maker(auth_config: AuthConfig) -> Callable[[str], str]:
    exp_delta = timedelta(minutes=auth_config.access_token_exp_minutes)

    expire = datetime.utcnow() + exp_delta
    claims = {"exp": expire}

    return lambda email: jwt.encode(
        claims={"sub": email} | claims,
        key=auth_config.secret,
        algorithm=auth_config.alg,
    )


@pytest.fixture
def access_token_default(access_token_maker: Callable[[str], str]) -> str:
    return access_token_maker(DEFAULT_EMAIL)


@pytest.fixture
def auth_headers_default(access_token_default: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token_default}"}
