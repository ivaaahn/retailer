from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.future import select

from retailer.app.application import app
from retailer.app.models.signup_sessions import SignupSessionModel
from retailer.app.models.users import UserModel
from retailer.store.rmq import RMQAccessor
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
        db: AsyncEngine,
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

        async with db.begin() as conn:
            user.id = await save_user(conn, user)
            await save_signup_session(conn, session)

        await cli.post(self.URI, json={"email": self.EMAIL, "code": self.CODE})

        ss_t = SignupSessionModel.__table__
        stmt = select(ss_t).where(ss_t.c.email == self.EMAIL)
        async with db.begin() as conn:
            cursor = await conn.execute(stmt)

        received_attempts = cursor.first()["attempts_left"]
        expected_attempts = 2
        assert received_attempts == expected_attempts

        user_t = UserModel.__table__
        stmt = select(user_t).where(user_t.c.email == self.EMAIL)
        async with db.begin() as conn:
            cursor = await conn.execute(stmt)

        received_status = cursor.first()["is_active"]
        expected_status = True
        assert received_status == expected_status


class TestUserSignup:
    URI = "api/auth/signup"

    EMAIL = "test@test.com"
    PASSWORD = "test"

    async def test_signup(
        self, db: AsyncConnection, rmq_store: RMQAccessor
    ) -> None:
        with TestClient(app) as client:
            res = client.post(
                self.URI,
                json={"email": self.EMAIL, "password": self.PASSWORD},
            )

        await rmq_store.connect()
        messages_count = await rmq_store.get_messages_count()
        await rmq_store.delete_queue()
        assert messages_count == 1

        data = res.json()
        received_email = data["email"]
        expected_email = self.EMAIL
        assert received_email == expected_email

        ss_t = SignupSessionModel.__table__
        stmt = select(ss_t).where(ss_t.c.email == self.EMAIL)
        cursor = await db.execute(stmt)
        received_attempts = cursor.first()["attempts_left"]
        expected_attempts = 3
        assert received_attempts == expected_attempts

        user_t = UserModel.__table__
        stmt = select(user_t).where(user_t.c.email == self.EMAIL)
        cursor = await db.execute(stmt)
        received_status = cursor.first()["is_active"]
        expected_status = False
        assert received_status == expected_status
