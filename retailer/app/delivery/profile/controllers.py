from fastapi import Depends, APIRouter

from app.delivery.auth.deps import get_current_active_user
from app.dto.profile import ProfileUpdateReqDTO
from app.dto.user import UserRespDTO
from app.services.profile import ProfileService

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)


@router.patch("", response_model=UserRespDTO)
async def patch(
    body: ProfileUpdateReqDTO,
    current_user: UserRespDTO = Depends(get_current_active_user),
    profile_service: ProfileService = Depends(),
):
    return await profile_service.patch(
        email=current_user.email,
        new_data=body,
    )
