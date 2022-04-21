from dataclasses import dataclass

from fastapi import Depends, Query
from pydantic import Field

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.products import ProductListSortByEnum


@dataclass
class ProductListPagingParams:
    base: BasePagingParams = Field(title="Параметры отображения на странице")
    sort_by: ProductListSortByEnum = Query(ProductListSortByEnum.id, max_length=50)


def product_paging_params(sort_by: ProductListSortByEnum, base: BasePagingParams = Depends(base_paging_params)):
    return ProductListPagingParams(base=base, sort_by=sort_by)
