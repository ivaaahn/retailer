from dataclasses import asdict

from app.base.services import BaseService
from app.delivery.products.errors import ProductNotFoundError
from app.dto.api.products import (
    ProductListPagingParams,
    ShopProductDTO,
    ShopProductsListDTO,
)
from app.dto.db.products import DBShopProductDTO
from app.repos.products import ProductsCacheRepo, ProductsRepo
from app.services.products.config import get_config
from fastapi import Depends

__all__ = ("ProductsService",)


class ProductsService(BaseService):
    def __init__(
        self,
        products_repo: ProductsRepo = Depends(),
        products_cache_repo: ProductsCacheRepo = Depends(),
    ):
        super().__init__()
        self._products_repo = products_repo
        self._products_cache_repo = products_cache_repo
        self._config = get_config()

    @staticmethod
    def _make_s3_url(path: str) -> str:
        return f"/img/{path}" if path else None

    async def __fetch_with_cache(
        self,
        product_id: int,
        shop_id: int,
    ) -> DBShopProductDTO:
        try:
            shop_product = await self._products_cache_repo.get(
                product_id, shop_id
            )
        except ProductNotFoundError:
            shop_product = await self._products_repo.get(product_id, shop_id)
            await self._products_cache_repo.save(
                product_id, shop_id, shop_product
            )

        return shop_product

    async def get(
        self,
        product_id: int,
        shop_id: int,
        *,
        use_cache: bool = True,
        as_db_dto: bool = False,
    ) -> ShopProductDTO | DBShopProductDTO:
        use_cache = self._config.use_cache and use_cache

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
                    availability=product.availability,
                )
                for product in res.products
            ],
            total=res.total,
        )
