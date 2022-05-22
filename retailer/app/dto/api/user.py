from datetime import datetime, date
from typing import Optional

from pydantic import EmailStr, BaseModel, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(title="Email (логин)")


class PasswordMixin(BaseModel):
    password: str = Field(title="Пароль")


class UserRespDTO(EmailMixin):
    id: int = Field(title="Идентификатор пользователя в базе данных")
    created_at: datetime = Field(title="Дата и время создания аккаунта")
    is_active: bool = Field(title="Признак активного аккаунта")
    name: Optional[str] = Field(title="Имя")
    birthday: Optional[date] = Field(title="Дата рождения")


class UserInDBSchema(UserRespDTO, PasswordMixin):
    pass
