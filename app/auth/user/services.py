from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from base.services import BaseService
from core.settings import get_settings
from .models import WebUsers
from .repos import AuthUserRepo
from .schemas import TokenDataSchema, UserSchema
from .settings import AuthSettings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthUserService(BaseService):
    @property
    def cfg(self) -> AuthSettings:
        return get_settings().auth

    async def signup_user(self, email: str, pwd: str) -> str:
        hashed_pwd = self._get_password_hash(pwd)

        email = await AuthUserRepo().add(email=email, password=hashed_pwd)

        if email is None:
            raise HTTPException(
                status_code=409, detail="User with this email already exist"
            )

        return email

    async def login_user(self, email: str, pwd: str) -> tuple[str, str]:
        user = await self._authenticate_user(email, pwd)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=self.cfg.access_token_exp_minutes)
        access_token = self._create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires,
        )
        return access_token, "bearer"

    async def get_current_user(self, token: str) -> UserSchema:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.cfg.secret, algorithms=[self.cfg.alg])
            email: str = payload.get("sub")

            if email is None:
                raise credentials_exception

            token_data = TokenDataSchema(email=email)
        except JWTError:
            raise credentials_exception

        user = await AuthUserRepo().get(token_data.email)

        if not user:
            raise credentials_exception

        return UserSchema.parse_obj(user)

    @staticmethod
    def _get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def _authenticate_user(self, email: str, pwd: str) -> Optional[WebUsers]:
        user = await AuthUserRepo().get(email)

        if not user:
            return None

        if not self._verify_password(
            plain_password=pwd,
            hashed_password=user.password,
        ):
            return None

        return user

    def _create_access_token(
        self, data: dict, expires_delta: timedelta = timedelta(minutes=15)
    ):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, self.cfg.secret, algorithm=self.cfg.alg)
