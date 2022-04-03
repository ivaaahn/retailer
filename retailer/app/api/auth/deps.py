from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.services import AuthService
from .schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth.login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends()
):
    return await auth_service.get_current_user(token)


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user
