from dataclasses import asdict

from fastapi import Depends, Query

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.api.products import ProductListSortByEnum, ProductListPagingParams


def product_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: ProductListSortByEnum = Query(default=ProductListSortByEnum.id),
) -> ProductListPagingParams:
    return ProductListPagingParams(**asdict(base), sort_by=sort_by)
