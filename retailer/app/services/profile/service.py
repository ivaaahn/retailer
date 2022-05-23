from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.dto.api.profile import ProfileUpdateReqDTO, AddressAddReqDTO
from app.dto.api.user import UserRespDTO, UserAddressDTO
from app.repos import IUsersRepo, UsersRepo

__all__ = ("ProfileService",)


@lru_cache
class ProfileService(BaseService):
    def __init__(
        self,
        users_repo: IUsersRepo = Depends(UsersRepo),
    ):
        super().__init__()
        self._users_repo = users_repo

    async def patch(self, email: str, new_data: ProfileUpdateReqDTO) -> UserRespDTO:
        updated = await self._users_repo.update(
            email=email,
            **new_data.dict(exclude_unset=True),
        )

        return UserRespDTO(**updated.as_dict())

    async def put(self, user_id: int, new_addr: AddressAddReqDTO) -> UserAddressDTO:
        addr_id = await self._users_repo.add(
            user_id=user_id,
            city=new_addr.city,
            street=new_addr.street,
            house=new_addr.house,
            entrance=new_addr.entrance,
            floor=new_addr.floor,
            flat=new_addr.flat,
        )
        return UserAddressDTO(address_id=addr_id)
