from app.dto.api.user import UserRespDTO
from app.services import AuthService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .errors import InactiveAccountError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()
) -> UserRespDTO:
    return await auth_service.get_current_user(token)


async def get_current_active_user(
    current_user: UserRespDTO = Depends(get_current_user),
) -> UserRespDTO:
    if not current_user.is_active:
        raise InactiveAccountError

    return current_user
