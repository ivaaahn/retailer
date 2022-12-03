from dataclasses import asdict

from fastapi import Depends, Query

from retailer.app.base.deps import BasePagingParams, base_paging_params
from retailer.app.dto.api.products import (
    ProductListPagingParams,
    ProductListSortByEnum,
)


def product_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: ProductListSortByEnum = Query(default=ProductListSortByEnum.id),
) -> ProductListPagingParams:
    return ProductListPagingParams(**asdict(base), sort_by=sort_by)
