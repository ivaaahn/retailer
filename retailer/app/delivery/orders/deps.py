from dataclasses import asdict

from fastapi import Depends, Query

from retailer.app.base.deps import BasePagingParams, base_paging_params
from retailer.app.dto.api.orders import (
    OrderListPagingParams,
    OrderListSortByEnum,
)


def order_paging_params(
    base: BasePagingParams = Depends(base_paging_params),
    sort_by: OrderListSortByEnum = Query(default=OrderListSortByEnum.id),
) -> OrderListPagingParams:
    return OrderListPagingParams(**asdict(base), sort_by=sort_by)
