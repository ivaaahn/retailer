import abc
from typing import Optional

from app.dto.db.profile import DBAddressListDTO
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

    @abc.abstractmethod
    async def add(
        self,
        user_id: int,
        city: str,
        street: str,
        house: str,
        entrance: int,
        floor: Optional[int],
        flat: Optional[str],
    ) -> int:
        pass

    @abc.abstractmethod
    async def get_list(self, user_id: int) -> DBAddressListDTO:
        pass
