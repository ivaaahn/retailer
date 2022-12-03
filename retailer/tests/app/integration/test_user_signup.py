from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.future import select

from retailer.app.application import app
from retailer.app.models.signup_sessions import SignupSessionModel
from retailer.app.models.users import UserModel
from retailer.store import rmq_accessor


class TestUserSignup:
    URI = "api/auth/signup"

    async def test_signup(self, db: AsyncConnection) -> None:
        email = "ivahnencko01@gmail.com"
        password = "test"

        with TestClient(app) as client:
            res = client.post(
                self.URI,
                json={"email": email, "password": password},
            )

        rmq = rmq_accessor()
        await rmq.connect()
        messages_count = await rmq.get_messages_count()
        await rmq.delete_queue()
        assert messages_count == 1

        data = res.json()
        received_email = data["email"]
        expected_email = email
        assert received_email == expected_email

        ss_t = SignupSessionModel.__table__
        stmt = select(ss_t).where(ss_t.c.email == email)
        cursor = await db.execute(stmt)
        received_attempts = cursor.first()["attempts_left"]
        expected_attempts = 3
        assert received_attempts == expected_attempts

        user_t = UserModel.__table__
        stmt = select(user_t).where(user_t.c.email == email)
        cursor = await db.execute(stmt)
        received_status = cursor.first()["is_active"]
        expected_status = False
        assert received_status == expected_status
