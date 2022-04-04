from pydantic import BaseModel, Field

from .user import EmailMixin, PasswordMixin


class SignupSchema(EmailMixin, PasswordMixin):
    pass


class SignupRespSchema(EmailMixin):
    pass


class LoginSchema(EmailMixin, PasswordMixin):
    pass


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(EmailMixin):
    pass


class VerifyCodeRequestSchema(EmailMixin):
    code: str = Field(title="Код")


class VerifyCodeRespSchema(EmailMixin):
    pass


class ResendCodeSchema(EmailMixin):
    pass


class ResendCodeRespSchema(EmailMixin):
    pass
