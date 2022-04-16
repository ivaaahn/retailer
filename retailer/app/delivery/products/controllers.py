from fastapi import Depends, APIRouter

from app.dto.products import BaseProductRespDTO
from app.services import ProductsService

router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("", response_model=BaseProductRespDTO)
async def get_by_name(
    name: str,
    products_service: ProductsService = Depends(),
):
    return await products_service.get(
        name=name,
    )
