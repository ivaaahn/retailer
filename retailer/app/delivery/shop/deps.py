from dataclasses import dataclass

from fastapi import Depends, Query
from pydantic import Field

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.shop import ShopListSortByEnum


@dataclass
class ShopListPagingParams:
    base: BasePagingParams = Field(title="Параметры отображения на странице")
    sort_by: ShopListSortByEnum = Query(ShopListSortByEnum.id, max_length=50)


def shop_paging_params(sort_by: ShopListSortByEnum, base: BasePagingParams = Depends(base_paging_params)):
    return ShopListPagingParams(base=base, sort_by=sort_by)
