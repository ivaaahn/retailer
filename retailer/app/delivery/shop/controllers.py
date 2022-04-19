from fastapi import Depends, APIRouter

from app.base.deps import OffsetDTO, get_offset
from app.dto.shop import ShopRespDTO, ShopListRespDTO, ShopAddressDTO

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
)


@router.get("", response_model=ShopRespDTO)
async def get_shop(
    _id: int,
):
    return ShopRespDTO(
        id=_id, address=ShopAddressDTO(id=_id, city="Moscow", street="popa", house=2)
    )


@router.get(".list", response_model=ShopListRespDTO)
async def get_list(query: OffsetDTO = Depends(get_offset)):
    return ShopListRespDTO(
        shops=[
            ShopRespDTO(
                id=0,
                address=ShopAddressDTO(id=0, city="Moscow", street="popa", house=2),
            ),
            ShopRespDTO(
                id=1,
                address=ShopAddressDTO(id=1, city="Moscow", street="jopa", house=33),
            ),
        ]
    )
