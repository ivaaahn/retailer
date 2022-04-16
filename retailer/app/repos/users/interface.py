import abc
from typing import Optional

from app.models.users import UserModel


class IUsersRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, email: str, **kwargs) -> Optional[UserModel]:
        pass

    @abc.abstractmethod
    async def upsert(self, email: str, password: str, **kwargs) -> UserModel:
        pass

    @abc.abstractmethod
    async def get(self, email: str, only_active: bool = True) -> Optional[UserModel]:
        pass
