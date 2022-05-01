from dataclasses import dataclass, asdict

from fastapi import Depends, Query
from pydantic import Field

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.shop import ShopListSortByEnum, ShopListPagingParams


def shop_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: ShopListSortByEnum = Query(default=ShopListSortByEnum.id),
) -> ShopListPagingParams:
    return ShopListPagingParams(**asdict(base), sort_by=sort_by)
