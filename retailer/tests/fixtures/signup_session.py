import pytest

from retailer.tests.builders.db.signup_session import DBSignupSessionBuilder


@pytest.fixture
def default_signup_session_to_build() -> DBSignupSessionBuilder:
    return DBSignupSessionBuilder()
