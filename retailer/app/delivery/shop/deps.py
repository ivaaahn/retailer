from dataclasses import dataclass, asdict

from fastapi import Depends, Query
from pydantic import Field

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.shop import ShopListSortByEnum


@dataclass
class ShopListPagingParams(BasePagingParams):
    sort_by: ShopListSortByEnum


def shop_paging_params(
    base=Depends(base_paging_params),
    sort_by: ShopListSortByEnum = ShopListSortByEnum.id,
):
    return ShopListPagingParams(**asdict(base), sort_by=sort_by)
