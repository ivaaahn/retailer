from dataclasses import dataclass
from enum import Enum

from fastapi import Query


class SortOrderEnum(str, Enum):
    desc = "desc"
    asc = "asc"


@dataclass
class BasePagingParams:
    count: int
    offset: int
    order: SortOrderEnum


def base_paging_params(
    count: int, offset: int, order: SortOrderEnum = Query(default=SortOrderEnum.desc)
) -> BasePagingParams:
    return BasePagingParams(count=count, offset=offset, order=order)
