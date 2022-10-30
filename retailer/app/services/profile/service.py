from dataclasses import asdict

from fastapi import Depends

from app.base.services import BaseService
from app.dto.api.profile import AddressAddDTO, ProfileUpdateReqDTO, UserAddressListDTO
from app.dto.api.user import UserAddressDTO, UserRespDTO
from app.repos.users import UsersRepo

__all__ = ("ProfileService",)


class ProfileService(BaseService):
    def __init__(
        self,
        users_repo: UsersRepo = Depends(),
    ):
        super().__init__()
        self._users_repo = users_repo

    async def patch(self, email: str, new_data: ProfileUpdateReqDTO) -> UserRespDTO:
        updated = await self._users_repo.update(
            email=email,
            **new_data.dict(exclude_unset=True),
        )

        return UserRespDTO(**asdict(updated))

    async def add_address(
        self, user_id: int, new_addr: AddressAddDTO
    ) -> UserAddressDTO:
        addr_id = await self._users_repo.add_address(
            user_id=user_id,
            city=new_addr.city,
            street=new_addr.street,
            house=new_addr.house,
            entrance=new_addr.entrance,
            floor=new_addr.floor,
            flat=new_addr.flat,
        )
        return UserAddressDTO(address_id=addr_id)

    async def get_addresses_list(self, user_id: int) -> UserAddressListDTO:
        addresses = await self._users_repo.get_addresses_list(user_id)

        return UserAddressListDTO(**asdict(addresses))
