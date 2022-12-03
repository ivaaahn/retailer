from abc import ABC, abstractmethod

from retailer.app.dto.db.signup_session import DBSignupSessionDTO
from retailer.app.dto.db.user import DBUserDTO


class IUserRepo(ABC):
    @abstractmethod
    async def update(self, email: str, **kwargs) -> DBUserDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, email: str, password: str, **kwargs) -> DBUserDTO:
        raise NotImplementedError

    @abstractmethod
    async def get(
        self, email: str, only_active: bool = True
    ) -> DBUserDTO | None:
        raise NotImplementedError


class ISignupSessionRepo(ABC):
    @abstractmethod
    async def get(self, email: str) -> DBSignupSessionDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert(
        self, email: str, code: str, **kwargs
    ) -> DBSignupSessionDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_code(self, email: str, code: str) -> DBSignupSessionDTO:
        raise NotImplementedError

    @abstractmethod
    async def update(self, email: str, **kwargs) -> DBSignupSessionDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def waste_attempt(self, email: str) -> DBSignupSessionDTO:
        raise NotImplementedError


class IRMQInteractRepo(ABC):
    @abstractmethod
    async def send_code(self, email: str, code: str):
        raise NotImplementedError

    @abstractmethod
    async def send_accept(self, email: str, order_id: int):
        raise NotImplementedError
