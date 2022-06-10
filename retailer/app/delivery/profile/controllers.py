from fastapi import APIRouter, Depends

from app.delivery.auth.deps import get_current_active_user
from app.dto.api.profile import AddressAddDTO, ProfileUpdateReqDTO, UserAddressListDTO
from app.dto.api.user import UserAddressDTO, UserRespDTO
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
) -> UserRespDTO:
    return await profile_service.patch(
        email=current_user.email,
        new_data=body,
    )


@router.put("/address", response_model=UserAddressDTO)
async def put(
    body: AddressAddDTO,
    user: UserRespDTO = Depends(get_current_active_user),
    profile_service: ProfileService = Depends(),
) -> UserAddressDTO:
    return await profile_service.add_address(user_id=user.id, new_addr=body)


@router.get("/address", response_model=UserAddressListDTO)
async def get_list(
    user: UserRespDTO = Depends(get_current_active_user),
    profile_service: ProfileService = Depends(),
) -> UserAddressListDTO:
    return await profile_service.get_addresses_list(user.id)
