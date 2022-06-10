from fastapi import APIRouter, Depends

from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.api.products import ShopProductDTO, ShopProductsListDTO
from app.services import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["product"],
)


@router.get("/{product_id}", response_model=ShopProductDTO)
async def get(
    product_id: int, shop_id: int, product_service: ProductsService = Depends()
) -> ShopProductDTO:
    return await product_service.get(product_id, shop_id)


@router.get("", response_model=ShopProductsListDTO)
async def get_list(
    shop_id: int,
    paging_params: ProductListPagingParams = Depends(product_paging_params),
    product_service: ProductsService = Depends(),
) -> ShopProductsListDTO:
    return await product_service.get_list(shop_id, paging_params)
