from functools import lru_cache

from fastapi import Depends

from base.services import BaseService
from dto.profile import ProfileUpdateSchema
from dto.user import UserSchema
from repos import IUsersRepo, UsersRepo


@lru_cache
class ProfileService(BaseService):
    def __init__(
        self,
        users_repo: IUsersRepo = Depends(UsersRepo),
    ):
        self._users_repo = users_repo

    async def patch(self, email: str, new_data: ProfileUpdateSchema) -> UserSchema:
        updated = await self._users_repo.update(
            email=email,
            **new_data.dict(exclude_unset=True),
        )

        return UserSchema(**updated.as_dict())
