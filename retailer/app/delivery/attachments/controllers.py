from fastapi import Depends, APIRouter

from app.delivery.products.deps import ProductListPagingParams, product_paging_params
from app.dto.products import ShopProductsListDTO, ShopProductDTO
from app.services.attachments.service import AttachmentsService

router = APIRouter(
    prefix="/attachments",
    tags=["attachments"],
)


@router.get("/s3/download")
async def get(path: str, attachment_service: AttachmentsService = Depends()):
    return await attachment_service.download_from_s3(path)
