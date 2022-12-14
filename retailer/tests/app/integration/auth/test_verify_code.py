from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.models.signup_sessions import SignupSessionModel
from retailer.app.models.users import UserModel
from retailer.tests.builders.db.signup_session import (
    DBSignupSessionBuilder,
    save_signup_session,
)
from retailer.tests.builders.db.user import DBUserBuilder, save_user


class TestVerifyCode:
    URI = "api/auth/verify_code"

    EMAIL = "test@test.com"
    PASSWORD = "test"
    CODE = "12345678"

    async def test_success(
        self,
        engine: AsyncEngine,
        cli: AsyncClient,
        default_user_to_build: DBUserBuilder,
        default_signup_session_to_build: DBSignupSessionBuilder,
    ) -> None:
        user = (
            default_user_to_build.but()
            .with_email(self.EMAIL)
            .with_password(self.PASSWORD)
            .build()
        )
        session = (
            default_signup_session_to_build.but()
            .with_code(self.CODE)
            .with_email(self.EMAIL)
            .build()
        )

        async with engine.begin() as conn:
            user_saved = await save_user(conn, user)
            await save_signup_session(conn, session)

        response = await cli.post(
            self.URI, json={"email": self.EMAIL, "code": self.CODE}
        )
        assert response.is_success

        session_table = SignupSessionModel.__table__
        stmt = select(session_table).where(session_table.c.email == self.EMAIL)
        async with engine.begin() as conn:
            cursor = await conn.execute(stmt)

        expected_attempts = 2
        received_attempts = cursor.first()["attempts_left"]
        assert received_attempts == expected_attempts

        user_table = UserModel.__table__
        stmt = select(user_table).where(user_table.c.email == self.EMAIL)
        async with engine.begin() as conn:
            cursor = await conn.execute(stmt)

        expected_status = True
        received_status = cursor.first()["is_active"]
        assert received_status == expected_status
