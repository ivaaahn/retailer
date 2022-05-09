from pydantic import BaseModel, Field

from .user import EmailMixin, PasswordMixin


class SignupReqDTO(EmailMixin, PasswordMixin):
    pass


class SignupRespDTO(EmailMixin):
    seconds_left: int = Field(
        title="Оставшееся кол-во секунд до возможности повторно отправить код"
    )


class LoginRequestDTO(EmailMixin, PasswordMixin):
    pass


class TokenRespDTO(BaseModel):
    access_token: str
    token_type: str


class TokenDataDTO(EmailMixin):
    pass


class VerifyCodeReqDTO(EmailMixin):
    code: str = Field(title="Код")


class VerifyCodeRespSchema(EmailMixin):
    pass


class ResendCodeReqDTO(EmailMixin):
    pass


class ResendCodeRespDTO(EmailMixin):
    seconds_left: int = Field(
        title="Оставшееся кол-во секунд до возможности повторно отправить код"
    )
