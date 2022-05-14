from dataclasses import asdict
from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.delivery.products.deps import product_paging_params
from app.delivery.products.errors import ProductNotFoundError
from app.dto.api.products import (
    ShopProductDTO,
    ProductListPagingParams,
    ShopProductsListDTO,
)
from app.dto.db.products import DBShopProductDTO
from app.repos.products import (
    IProductsRepo,
    ProductsRepo,
    ProductsCacheRepo,
    IProductsCacheRepo,
)

__all__ = ("ProductsService",)


@lru_cache
class ProductsService(BaseService):
    def __init__(
        self,
        products_repo: IProductsRepo = Depends(ProductsRepo),
        products_cache_repo: IProductsCacheRepo = Depends(ProductsCacheRepo),
    ):
        super().__init__()
        self._products_repo = products_repo
        self._products_cache_repo = products_cache_repo

    @staticmethod
    def _make_s3_url(path: str) -> str:
        return f"/img/{path}" if path else None

    async def __fetch_with_cache(
        self,
        product_id: int,
        shop_id: int,
    ) -> DBShopProductDTO:
        try:
            shop_product = await self._products_cache_repo.get(product_id, shop_id)
        except ProductNotFoundError:
            shop_product = await self._products_repo.get(product_id, shop_id)
            await self._products_cache_repo.save(product_id, shop_id, shop_product)

        return shop_product

    async def get(
        self,
        product_id: int,
        shop_id: int,
        *,
        use_cache: bool = True,
        as_db_dto: bool = False,
    ) -> ShopProductDTO | DBShopProductDTO:
        if not use_cache:
            shop_product = await self._products_repo.get(product_id, shop_id)
        else:
            shop_product = await self.__fetch_with_cache(product_id, shop_id)

        shop_product.photo = self._make_s3_url(shop_product.photo)
        if as_db_dto:
            return shop_product

        return ShopProductDTO(**asdict(shop_product))

    async def get_list(
        self,
        shop_id: int,
        paging_params: ProductListPagingParams,
    ) -> ShopProductsListDTO:
        res = await self._products_repo.get_list(shop_id, paging_params)

        return ShopProductsListDTO(
            products=[
                ShopProductDTO(
                    id=product.id,
                    photo=self._make_s3_url(product.photo),
                    name=product.name,
                    description=product.description,
                    price=product.price,
                    category=product.category,
                    qty=product.availability,
                )
                for product in res.products
            ],
            total=res.total,
        )
