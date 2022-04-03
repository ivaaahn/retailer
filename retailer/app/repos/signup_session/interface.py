import abc
from typing import Optional

from app.models import SignupSession


class ISignupSessionRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, email: str) -> Optional[SignupSession]:
        pass

    @abc.abstractmethod
    async def upsert(self, email: str, code: str, **kwargs) -> SignupSession:
        pass

    @abc.abstractmethod
    async def update(self, email: str, **kwargs) -> Optional[SignupSession]:
        pass

    @abc.abstractmethod
    async def update_code(self, email: str, code: str) -> SignupSession:
        pass

    @abc.abstractmethod
    async def waste_attempt(self, email: str) -> SignupSession:
        pass
