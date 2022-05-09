from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.dto.api.profile import ProfileUpdateReqDTO
from app.dto.api.user import UserRespDTO
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
