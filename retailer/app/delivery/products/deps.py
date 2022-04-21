from dataclasses import dataclass, asdict

from fastapi import Depends, Query
from pydantic import Field

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.products import ProductListSortByEnum


@dataclass
class ProductListPagingParams(BasePagingParams):
    sort_by: ProductListSortByEnum


def product_paging_params(
    base=Depends(base_paging_params),
    sort_by: ProductListSortByEnum = ProductListSortByEnum.id,
):
    return ProductListPagingParams(**asdict(base), sort_by=sort_by)
