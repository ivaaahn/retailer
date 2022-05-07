from fastapi import Depends, APIRouter

from app.delivery.shop.deps import shop_paging_params
from app.dto.api.shop import (
    ShopRespDTO,
    ShopListRespDTO,
    ShopListPagingParams,
    ShopAddressDTO,
)
from app.services.shop import ShopsService

router = APIRouter(
    prefix="/shop",
    tags=["shop"],
)


@router.get("", response_model=ShopRespDTO)
async def get_shop(id: int, shop_service: ShopsService = Depends()) -> ShopRespDTO:
    return await shop_service.get_shop(id)


@router.get(".list", response_model=ShopListRespDTO)
async def get_list(
    shop_service: ShopsService = Depends(),
    paging_params: ShopListPagingParams = Depends(shop_paging_params),
) -> ShopListRespDTO:
    return await shop_service.get_list(paging_params)
