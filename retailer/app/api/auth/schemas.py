from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(title="Email (логин)")


class PasswordMixin(BaseModel):
    password: str = Field(title="Пароль")


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
class VerifyCodeRequestSchema(EmailMixin):
    code: str = Field(title="Код")


class VerifyCodeRespSchema(EmailMixin):
    pass


class ResendCodeSchema(EmailMixin):
    pass


class ResendCodeRespSchema(EmailMixin):
    pass
