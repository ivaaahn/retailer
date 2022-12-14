from dataclasses import asdict

import pytest

from retailer.app.base.deps import SortOrderEnum
from retailer.app.dto.api.products import (
    ProductListPagingParams,
    ProductListSortByEnum,
    ShopProductDTO,
    ShopProductsListDTO,
)
from retailer.app.dto.db.products import DBShopProductListDTO
from retailer.app.services import ProductsService
from retailer.tests.builders.db.product import DBShopProductBuilder
from retailer.tests.builders.db.shops import DBShopBuilder
from retailer.tests.constants import DEFAULT_S3_URL
from retailer.tests.mocks import ProductsCacheRepoMock, ProductsRepoMock


@pytest.fixture
def default_product_to_build() -> DBShopProductBuilder:
    return DBShopProductBuilder()


@pytest.fixture
def default_product_s3_patched_to_build() -> DBShopProductBuilder:
    return DBShopProductBuilder().but().with_photo(DEFAULT_S3_URL)


@pytest.fixture
def default_products_list_built(
    default_product_to_build: DBShopProductBuilder,
) -> DBShopProductListDTO:
    qty = 2
    products = [
        default_product_to_build.but().with_id(idx).build()
        for idx in range(1, qty + 1)
    ]

    return DBShopProductListDTO(
        total=qty,
        products=products,
    )


@pytest.fixture
def default_products_list_s3_patched_built(
    default_products_list_built: DBShopProductListDTO,
) -> ShopProductsListDTO:
    return ShopProductsListDTO(
        total=default_products_list_built.total,
        products=[
            ShopProductDTO(**asdict(p) | dict(photo=DEFAULT_S3_URL))
            for p in default_products_list_built.products
        ],
    )


@pytest.fixture
def default_paging_params() -> ProductListPagingParams:
    return ProductListPagingParams(
        count=100,
        offset=0,
        order=SortOrderEnum.asc,
        sort_by=ProductListSortByEnum.id,
    )


@pytest.fixture
def products_service(
    products_repo_mock: ProductsRepoMock,
    products_cache_repo_mock: ProductsCacheRepoMock,
) -> ProductsService:
    return ProductsService(
        products_repo=products_repo_mock,
        products_cache_repo=products_cache_repo_mock,
    )
