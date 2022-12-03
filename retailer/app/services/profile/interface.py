from abc import ABC, abstractmethod

from retailer.app.dto.db.profile import DBAddressListDTO
from retailer.app.dto.db.user import DBUserDTO


class IUsersRepo(ABC):
    @abstractmethod
    async def get_addresses_list(self, user_id: int) -> DBAddressListDTO:
        pass

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
        pass

    @abstractmethod
    async def update(self, email: str, **kwargs) -> DBUserDTO | None:
        pass
