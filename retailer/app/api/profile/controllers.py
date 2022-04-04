from fastapi import Depends, APIRouter

from api.auth.deps import get_current_active_user
from dto.profile import ProfileUpdateSchema
from dto.user import UserSchema
from services.profile import ProfileService

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
