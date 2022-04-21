from dataclasses import dataclass
from enum import Enum

from fastapi import Query


class SortOrderEnum(str, Enum):
    desc = "desc"
    asc = "asc"


@dataclass
class BasePagingParams:
    count: int = Query(None, le=50, description="description")
    offset: int = Query(None, le=50)
    order: SortOrderEnum = Query(SortOrderEnum.desc, max_length=50)


def base_paging_params(count: int, offset: int, order: SortOrderEnum):
    return BasePagingParams(count=count, offset=offset, order=order)
