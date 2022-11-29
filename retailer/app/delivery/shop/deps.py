from dataclasses import asdict

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.api.shop import ShopListPagingParams, ShopListSortByEnum
from fastapi import Depends, Query


def shop_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: ShopListSortByEnum = Query(default=ShopListSortByEnum.id),
) -> ShopListPagingParams:
    return ShopListPagingParams(**asdict(base), sort_by=sort_by)
