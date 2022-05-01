from dataclasses import dataclass, asdict

from fastapi import Depends, Query

from app.base.deps import BasePagingParams, base_paging_params
from app.dto.orders import OrderListPagingParams, OrderListSortByEnum
from app.dto.products import ProductListSortByEnum


def order_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: OrderListSortByEnum = Query(default=OrderListSortByEnum.id),
) -> OrderListPagingParams:
    return OrderListPagingParams(**asdict(base), sort_by=sort_by)
