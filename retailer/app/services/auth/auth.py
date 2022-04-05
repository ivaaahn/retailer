import random
import string
from datetime import timedelta, datetime
from functools import lru_cache

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from base.errors import check_err, DBErrEnum
from base.services import BaseService
from app.api.auth.errors import (
    UserNotFoundError,
    SignupSessionCreateTimeoutNotExpired,
    UserAlreadyExistsError,
    IncorrectCredsError,
    InactiveAccountError,
    IncorrectLoginCredsError,
    IncorrectCodeError,
)
from app.dto.signup import TokenDataSchema
from app.dto.user import UserSchema
from app.models import Users, SignupSession
from app.repos import (
    IRMQInteractRepo,
    ISignupSessionRepo,
    IUsersRepo,
    RMQInteractRepo,
    SignupSessionRepo,
    UsersRepo,
)
from .settings import AuthSettings, get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO fix lru cache unhashble
class AuthService(BaseService):
    def __init__(
        self,
        settings: AuthSettings = Depends(get_settings),
        users_repo: IUsersRepo = Depends(UsersRepo),
        signup_session_repo: ISignupSessionRepo = Depends(SignupSessionRepo),
        rmq_interact_repo: IRMQInteractRepo = Depends(RMQInteractRepo),
    ):
        super().__init__()
        self._settings = settings
        self._users_repo = users_repo
        self._signup_session_repo = signup_session_repo
        self._rmq_interact_repo = rmq_interact_repo

    @property
    def cfg(self) -> AuthSettings:
        return self._settings

    async def signup_user(self, email: str, pwd: str) -> str:
        hashed_pwd = self._get_password_hash(pwd)

        active_user = await self._users_repo.get(email, only_active=True)
        if active_user:
            raise UserAlreadyExistsError(email)

        web_user = await self._users_repo.upsert(email=email, password=hashed_pwd)
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

        user = await self._users_repo.get(token_data.email, only_active=False)
        if not user:
            raise IncorrectCredsError

        return UserSchema.parse_obj(user.as_dict())

    async def verify_code(self, email: str, code: str) -> str:
        session = await self._signup_session_repo.waste_attempt(email)

        if session.code != code:
            raise IncorrectCodeError(session.attempts_left)

        user = await self._activate_user(email)
        return user.email

    async def _activate_user(self, email: str) -> Users:
        return await self._users_repo.update(email=email, is_active=True)

    async def resend_code(self, email: str) -> str:
        signup_session = await self._resend_code(email)
        return signup_session.email

    async def _check_session_and_send_code(self, email: str) -> str:
        await self._check_session_expiration(email)
        code = self._generate_code()
        await self._rmq_interact_repo.send_code(email, code)
        return code

    async def _send_code(self, email: str) -> SignupSession:
        code = await self._check_session_and_send_code(email)
        return await self._signup_session_repo.upsert(email, code)

    async def _resend_code(self, email: str) -> SignupSession:
        code = await self._check_session_and_send_code(email)

        try:
            signup_session = await self._signup_session_repo.update_code(email, code)
        except IntegrityError as err:
            if check_err(err, DBErrEnum.foreign_key_violation):
                raise UserNotFoundError(email)
            raise err

        return signup_session

    async def _check_session_expiration(self, email: str) -> SignupSession:
        session = await self._signup_session_repo.get(email)
        if session and not session.send_code_timeout_expired:
            raise SignupSessionCreateTimeoutNotExpired(session.seconds_left)

        return session

    @staticmethod
    def _generate_code(length: int = 8) -> str:
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def _authenticate_user(self, email: str, pswd: str) -> Users:
        user = await self._users_repo.get(email, only_active=False)

        if not user or not self._verify_password(
            plain_password=pswd,
            hashed_password=user.password,
        ):
            raise IncorrectLoginCredsError

        return user

    def _create_access_token(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.cfg.secret, algorithm=self.cfg.alg)
