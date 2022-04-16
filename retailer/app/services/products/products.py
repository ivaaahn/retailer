from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.delivery.products.errors import ProductNotFoundError
from app.dto.products import BaseProductRespDTO
from app.repos.products import IProductsRepo, ProductsRepo

__all__ = ("ProductsService",)


@lru_cache
class ProductsService(BaseService):
    def __init__(
        self,
        products_repo: IProductsRepo = Depends(ProductsRepo),
    ):
        super().__init__()
        self._products_repo = products_repo

    async def get(self, name: str) -> BaseProductRespDTO:
        received = await self._products_repo.get(name)
        if not received:
            raise ProductNotFoundError(name)

        self.logger.debug(received.as_dict())

        return BaseProductRespDTO(
            name=received.name,
            description=received.description,
            category=received.category_name,
        )
