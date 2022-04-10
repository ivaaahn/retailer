from fastapi import Depends, APIRouter

from app.api.auth.deps import get_current_active_user
from app.dto.profile import ProfileUpdateSchema
from app.dto.user import UserSchema
from app.services.profile import ProfileService

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


@router.patch("/", response_model=UserSchema)
async def patch(
    body: ProfileUpdateSchema,
    current_user: UserSchema = Depends(get_current_active_user),
    profile_service: ProfileService = Depends(),
):
    print(body)
    return await profile_service.patch(
        email=current_user.email,
        new_data=body,
    )
