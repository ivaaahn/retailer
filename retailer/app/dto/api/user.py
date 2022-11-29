from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class EmailMixin(BaseModel):
    email: EmailStr = Field(title="Email (логин)")


class PasswordMixin(BaseModel):
    password: str = Field(title="Пароль")


class UserRespDTO(EmailMixin):
    id: int = Field(title="Идентификатор пользователя в базе данных")
    created_at: datetime = Field(title="Дата и время создания аккаунта")
    is_active: bool = Field(title="Признак активного аккаунта")
    name: str | None = Field(title="Имя")
    birthday: date | None = Field(title="Дата рождения")


class UserInDBSchema(UserRespDTO, PasswordMixin):
    pass


class UserAddressDTO(BaseModel):
    address_id: int = Field(title="Идентификатор адреса в базе данных")
