import abc
from typing import Optional

from app.models import Users


class IUsersRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def update(self, email: str, **kwargs) -> Optional[Users]:
        pass

    @abc.abstractmethod
    async def upsert(self, email: str, password: str, **kwargs) -> Users:
        pass

    @abc.abstractmethod
    async def get(self, email: str, only_active: bool = True) -> Optional[Users]:
        pass
