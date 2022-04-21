from enum import Enum

from fastapi import Depends, APIRouter

from app.base.deps import BasePagingParams
from app.delivery.shop.deps import ShopListPagingParams
from app.dto.shop import ShopRespDTO, ShopListRespDTO, ShopAddressDTO
from app.delivery.shop.deps import shop_paging_params

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
)


@router.get("", response_model=ShopRespDTO)
async def get_shop(
    id: int,
):
    return ShopRespDTO(
        id=id, address=ShopAddressDTO(id=id, city="Moscow", street="popa", house=2)
    )


@router.get(".list", response_model=ShopListRespDTO)
async def get_list(paging_params: ShopListPagingParams = Depends(shop_paging_params)):
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
        ],
        total=30,
    )
