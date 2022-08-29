import random
import string
from datetime import datetime, timedelta

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.base.errors import DBErrEnum, check_err
from app.base.services import BaseService
from app.delivery.auth.errors import (
    InactiveAccountError,
    IncorrectCodeError,
    IncorrectCredsError,
    IncorrectLoginCredsError,
    SignupSessionCreateTimeoutNotExpired,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.dto.api.signup import (
    ResendCodeRespDTO,
    SignupRespDTO,
    TokenDataDTO,
    TokenRespDTO,
)
from app.dto.api.user import UserRespDTO
from app.models.signup_sessions import SignupSessionModel
from app.models.users import UserModel
from app.repos import (
    RMQInteractRepo,
    SignupSessionRepo,
    UsersRepo,
)
from .config import AuthConfig, get_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

__all__ = ("AuthService",)


class AuthService(BaseService):
    def __init__(
        self,
        users_repo: UsersRepo = Depends(),
        signup_session_repo: SignupSessionRepo = Depends(),
        rmq_interact_repo: RMQInteractRepo = Depends(),
    ):
        super().__init__()
        self._config = get_config()
        self._users_repo = users_repo
        self._signup_session_repo = signup_session_repo
        self._rmq_interact_repo = rmq_interact_repo

    @property
    def cfg(self) -> AuthConfig:
        return self._config

    async def signup_user(self, email: str, pwd: str) -> SignupRespDTO:
        hashed_pwd = self._get_password_hash(pwd)

        active_user = await self._users_repo.get(email, only_active=True)
        if active_user:
            raise UserAlreadyExistsError(email)

        web_user = await self._users_repo.upsert(email=email, password=hashed_pwd)
        signup_session = await self._send_code(web_user.email)

        return SignupRespDTO(
            email=web_user.email, seconds_left=signup_session.seconds_left
        )

    async def resend_code(self, email: str) -> ResendCodeRespDTO:
        signup_session = await self._resend_code(email)
        return ResendCodeRespDTO(
            email=signup_session.email, seconds_left=signup_session.seconds_left
        )

    async def login_user(self, email: str, pwd: str) -> TokenRespDTO:
        user = await self._authenticate_user(email, pwd)
        if not user.is_active:
            raise InactiveAccountError

        access_token_expires = timedelta(minutes=self.cfg.access_token_exp_minutes)
        access_token = self._create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires,
        )
        await self._users_repo.update(email, last_login=datetime.utcnow())

        return TokenRespDTO(
            access_token=access_token,
            token_type="bearer",
        )

    async def get_current_user(self, token: str) -> UserRespDTO:
        try:
            payload = jwt.decode(token, self.cfg.secret, algorithms=[self.cfg.alg])
        except JWTError:
            raise IncorrectCredsError

        email = payload.get("sub")
        if email is None:
            raise IncorrectCredsError

        token_data = TokenDataDTO(email=email)
        user = await self._users_repo.get(token_data.email, only_active=False)
        if not user:
            raise IncorrectCredsError

        return UserRespDTO.parse_obj(user.as_dict())

    async def verify_code(self, email: str, code: str) -> str:
        session = await self._signup_session_repo.waste_attempt(email)

        if session.code != code:
            raise IncorrectCodeError(session.attempts_left)

        user = await self._activate_user(email)
        return user.email

    async def _activate_user(self, email: str) -> UserModel:
        return await self._users_repo.update(email=email, is_active=True)

    async def _check_session_and_send_code(self, email: str) -> str:
        await self._check_session_expiration(email)

        code = self._generate_code()
        self.logger.debug(f"Generated code: {code}")
        await self._rmq_interact_repo.send_code(email, code)

        return code

    async def _send_code(self, email: str) -> SignupSessionModel:
        code = await self._check_session_and_send_code(email)
        return await self._signup_session_repo.upsert(email, code)

    async def _resend_code(self, email: str) -> SignupSessionModel:
        code = await self._check_session_and_send_code(email)

        try:
            signup_session = await self._signup_session_repo.update_code(email, code)
        except IntegrityError as err:
            if check_err(err, DBErrEnum.foreign_key_violation):
                raise UserNotFoundError(email)
            raise err

        return signup_session

    async def _check_session_expiration(self, email: str) -> SignupSessionModel:
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

    async def _authenticate_user(self, email: str, pswd: str) -> UserModel:
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
