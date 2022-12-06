from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from retailer.app.models.signup_sessions import SignupSessionModel
from retailer.app.models.users import UserModel
from retailer.store.rmq import RMQAccessor


class TestUserSignup:
    URI = "api/auth/signup"

    EMAIL = "test@test.com"
    PASSWORD = "test"

    async def test_signup(
        self, engine: AsyncEngine, cli: AsyncClient, rmq_store: RMQAccessor
    ) -> None:
        raw_response = await cli.post(
            self.URI,
            json={"email": self.EMAIL, "password": self.PASSWORD},
        )

        expected_messages_count = 1
        received_message_count = await rmq_store.get_messages_count()
        await rmq_store.delete_queue()
        assert received_message_count == expected_messages_count

        response_data = raw_response.json()
        expected_email = self.EMAIL
        received_email = response_data["email"]
        assert received_email == expected_email

        session_table = SignupSessionModel.__table__
        stmt = select(session_table).where(session_table.c.email == self.EMAIL)
        async with engine.begin() as conn:
            cursor = await conn.execute(stmt)

        expected_attempts = 3
        received_attempts = cursor.first()["attempts_left"]
        assert received_attempts == expected_attempts

        user_table = UserModel.__table__
        stmt = select(user_table).where(user_table.c.email == self.EMAIL)
        async with engine.begin() as conn:
            cursor = await conn.execute(stmt)

        expected_status = False
        received_status = cursor.first()["is_active"]
        assert received_status == expected_status
