from fastapi import Depends, APIRouter

from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.products import ProductListRespDTO, ProductRespDTO

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("", response_model=ProductRespDTO)
async def get_by_shop(product_id: int, shop_id: int):
    return ProductRespDTO(name="кока-кола", category="напитки", price=99, qty=10)


@router.get(".list", response_model=ProductListRespDTO)
async def get_list(
    shop_id: int,
    paging_params: ProductListPagingParams = Depends(product_paging_params),
):
    return ProductListRespDTO(
        products=[
            ProductRespDTO(
                name="молоко",
                description="годен 3 дня после открытия",
                category="молочные продукты",
                price=88.5,
                qty=30,
            ),
            ProductRespDTO(name="кока-кола", category="напитки", price=99, qty=10),
        ],
        total=2,
    )
