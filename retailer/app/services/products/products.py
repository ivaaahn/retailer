from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.delivery.products.errors import ProductNotFoundError
from app.dto.products import ShopProductDTO
from app.repos.products import IProductsRepo, ProductsRepo
from app.services.attachments.service import AttachmentsService

__all__ = ("ProductsService",)


@lru_cache
class ProductsService(BaseService):
    def __init__(
        self,
        products_repo: IProductsRepo = Depends(ProductsRepo),
        attachments_service: AttachmentsService = Depends(AttachmentsService),
    ):
        super().__init__()
        self._products_repo = products_repo
        self._attachments_service = attachments_service

    async def get(self, name: str) -> ShopProductDTO:
        received = await self._products_repo.get(name)
        if not received:
            raise ProductNotFoundError(name)

        self.logger.debug(received.as_dict())

        return ShopProductDTO(
            id=received.id,
            name=received.name,
            description=received.description,
            category=received.category_name,
            photo=self._attachments_service.make_s3_url(received.photo),
        )
