from dataclasses import asdict

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.api.products import ProductListPagingParams, ProductListSortByEnum
from fastapi import Depends, Query


def product_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: ProductListSortByEnum = Query(default=ProductListSortByEnum.id),
) -> ProductListPagingParams:
    return ProductListPagingParams(**asdict(base), sort_by=sort_by)
