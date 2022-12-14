from collections.abc import Callable

import pytest
import pytz
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.models.users import UserModel
from retailer.app.services.auth.service import pwd_context
from retailer.tests.builders.db.user import DBUserBuilder, save_user
from retailer.tests.constants import DEFAULT_DATETIME


class TestLogin:
    URI = "api/auth/login"

    EMAIL = "test@test.com"
    PASSWORD = "test"
    CODE = "12345678"

    @pytest.mark.freeze_time(DEFAULT_DATETIME)
    async def test_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_user_to_build: DBUserBuilder,
        access_token_maker: Callable[[str], str],
    ) -> None:
        user = (
            default_user_to_build.but()
            .with_email(self.EMAIL)
            .with_password(pwd_context.hash(self.PASSWORD))
            .with_is_active(True)
            .build()
        )
        async with engine.begin() as conn:
            await save_user(conn, user)

        response = await cli.post(
            self.URI, data={"username": self.EMAIL, "password": self.PASSWORD}
        )
        assert response.is_success

        expected_response = {
            "access_token": access_token_maker(self.EMAIL),
            "token_type": "bearer",
        }
        received_response = response.json()
        assert received_response == expected_response

        user_table = UserModel.__table__
        stmt = select(user_table).where(user_table.c.email == self.EMAIL)
        async with engine.begin() as conn:
            cursor = await conn.execute(stmt)

        expected_last_login = DEFAULT_DATETIME.astimezone(pytz.UTC)
        received_last_login = cursor.first()["last_login"]
        assert (
            received_last_login.isoformat() == expected_last_login.isoformat()
        )
