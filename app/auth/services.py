from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from starlette import status

from base.errors import check_err, DBErrEnum
from base.services import BaseService
from core.settings import get_settings, AuthSettings
from .errors import (
    UserNotFoundError,
    SignupSessionCreateTimeoutNotExpired,
    UserAlreadyExistsError,
    IncorrectCredsError,
    InactiveAccountError,
    IncorrectLoginCredsError,
    IncorrectCodeError,
)
from .models import WebUsers, SignupSession
from .repos import WebUserRepo, SignupSessionRepo
from .schemas import TokenDataSchema, UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService(BaseService):
    @property
    def cfg(self) -> AuthSettings:
        return get_settings().auth

    async def signup_user(self, email: str, pwd: str) -> str:
        hashed_pwd = self._get_password_hash(pwd)

        active_user = await WebUserRepo().get(email, only_active=True)
        if active_user:
            raise UserAlreadyExistsError(email)

        web_user = await WebUserRepo().upsert(email=email, password=hashed_pwd)
        await self._send_code(web_user.email)

        return web_user.email

    async def login_user(self, email: str, pwd: str) -> tuple[str, str]:
        user = await self._authenticate_user(email, pwd)
        if not user.is_active:
            raise InactiveAccountError

        access_token_expires = timedelta(minutes=self.cfg.access_token_exp_minutes)
        access_token = self._create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires,
        )
        return access_token, "bearer"

    async def get_current_user(self, token: str) -> UserSchema:
        try:
            payload = jwt.decode(token, self.cfg.secret, algorithms=[self.cfg.alg])
            email: str = payload.get("sub")

            if email is None:
                raise IncorrectCredsError

            token_data = TokenDataSchema(email=email)
        except JWTError:
            raise IncorrectCredsError

        user = await WebUserRepo().get(token_data.email, only_active=False)
        if not user:
            raise IncorrectCredsError

        return UserSchema.parse_obj(user.as_dict())

    @staticmethod
    async def verify_code(email: str, code: str) -> str:
        session = await SignupSessionRepo().waste_attempt(email)

        if session.code != code:
            raise IncorrectCodeError(session.attempts_left)

        email = await WebUserRepo().activate_account(email)
        return email

    async def _send_code(self, email: str) -> SignupSession:
        await self.check_session_expiration(email)
        code = self._generate_code()
        # send code here
        signup_session = await SignupSessionRepo().upsert(email, code)
        return signup_session

    async def _resend_code(self, email: str) -> SignupSession:
        await self.check_session_expiration(email)
        code = self._generate_code()
        # send code here

        try:
            signup_session = await SignupSessionRepo().update_code(email, code)
        except IntegrityError as err:
            if check_err(err, DBErrEnum.foreign_key_violation):
                raise UserNotFoundError(email)
            raise err

        return signup_session

    @staticmethod
    async def check_session_expiration(email: str) -> SignupSession:
        session = await SignupSessionRepo().get(email)
        if session and not session.send_code_timeout_expired:
            raise SignupSessionCreateTimeoutNotExpired(session.seconds_left)

        return session

    def _generate_code(self) -> str:
        return "FAKECODE"

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def _authenticate_user(self, email: str, pwd: str) -> WebUsers:
        web_user = await WebUserRepo().get(email, only_active=False)

        if not web_user or not self._verify_password(
            plain_password=pwd,
            hashed_password=web_user.password,
        ):
            raise IncorrectLoginCredsError

        return web_user

    def _create_access_token(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.cfg.secret, algorithm=self.cfg.alg)

    async def resend_code(self, email: str) -> str:
        signup_session = await self._resend_code(email)
        return signup_session.email
