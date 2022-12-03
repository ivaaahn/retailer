from fastapi import APIRouter, Depends

from retailer.app.delivery.shop.deps import shop_paging_params
from retailer.app.dto.api.shop import (
    ShopListPagingParams,
    ShopListRespDTO,
    ShopRespDTO,
)
from retailer.app.services.shop import ShopsService

router = APIRouter(
    prefix="/shops",
    tags=["shop"],
)


@router.get("/{shop_id}", response_model=ShopRespDTO)
async def get_shop(
    shop_id: int, shop_service: ShopsService = Depends()
) -> ShopRespDTO:
    return await shop_service.get(shop_id)


@router.get("", response_model=ShopListRespDTO)
async def get_list(
    shop_service: ShopsService = Depends(),
    paging_params: ShopListPagingParams = Depends(shop_paging_params),
) -> ShopListRespDTO:
    return await shop_service.get_list(paging_params)
