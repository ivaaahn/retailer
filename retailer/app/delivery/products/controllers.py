from enum import Enum

from fastapi import Depends, APIRouter

from app.base.deps import BasePagingParams
from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.products import ProductRespDTO, ProductListRespDTO
from app.services import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("", response_model=ProductRespDTO)
async def get_by_name(
    name: str,
    products_service: ProductsService = Depends(),
):
    return await products_service.get(
        name=name,
    )


@router.get(".list", response_model=ProductListRespDTO)
async def get_list(paging_params: ProductListPagingParams = Depends(product_paging_params)):
    return ProductListRespDTO(
        products=[
            ProductRespDTO(
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                withAvailability=True,
            ),
            ProductRespDTO(name="кока-кола", category="напитки", withAvailability=True),
        ],
        total=10,
    )
