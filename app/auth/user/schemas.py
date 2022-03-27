from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(description="Email (логин)")


class PasswordMixin(BaseModel):
    password: str = Field(description="Пароль")


class UserSchema(EmailMixin):
    created_at: datetime
    is_active: bool


class UserInDBSchema(UserSchema, PasswordMixin):
    pass


##########################################
class SignupSchema(EmailMixin, PasswordMixin):
    pass


class SignupRespSchema(EmailMixin):
    pass


##########################################


##########################################
class LoginSchema(EmailMixin, PasswordMixin):
    pass


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(EmailMixin):
    pass


##########################################
