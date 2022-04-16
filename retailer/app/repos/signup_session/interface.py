import abc
from typing import Optional

from app.models.signup_session import SignupSessionModel


class ISignupSessionRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, email: str) -> Optional[SignupSessionModel]:
        pass

    @abc.abstractmethod
    async def upsert(self, email: str, code: str, **kwargs) -> SignupSessionModel:
        pass

    @abc.abstractmethod
    async def update(self, email: str, **kwargs) -> Optional[SignupSessionModel]:
        pass

    @abc.abstractmethod
    async def update_code(self, email: str, code: str) -> SignupSessionModel:
        pass

    @abc.abstractmethod
    async def waste_attempt(self, email: str) -> SignupSessionModel:
        pass
