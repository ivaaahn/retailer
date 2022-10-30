from abc import ABC, abstractmethod

from app.dto.db.profile import DBAddressListDTO
from app.dto.db.signup_session import DBSignupSessionDTO
from app.dto.db.user import DBUserDTO


class IUserRepo(ABC):
    @abstractmethod
    async def get_addresses_list(self, user_id: int) -> DBAddressListDTO:
        raise NotImplementedError

    @abstractmethod
    async def add_address(
        self,
        user_id: int,
        city: str,
        street: str,
        house: str,
        entrance: int,
        floor: int | None,
        flat: str | None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update(self, email: str, **kwargs) -> DBUserDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, email: str, password: str, **kwargs) -> DBUserDTO:
        raise NotImplementedError

    @abstractmethod
    async def get(self, email: str, only_active: bool = True) -> DBUserDTO | None:
        raise NotImplementedError


class ISignupSessionRepo(ABC):
    @abstractmethod
    async def get(self, email: str) -> DBSignupSessionDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, email: str, code: str, **kwargs) -> DBSignupSessionDTO:
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
