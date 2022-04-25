from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from app.base.deps import BasePagingParams
from app.dto.products import ProductRespDTO


class OrderListSortByEnum(str, Enum):
    id = "id"
    date = "date"


@dataclass
class OrderListPagingParams(BasePagingParams):
    sort_by: OrderListSortByEnum


class OrderStatusEnum(str, Enum):
    new = "new"
    created = "created"
    verified = "verified"
    cancelled = "cancelled"
    ready = "ready"
    shipped = "shipped"
    delivered = "delivered"


class OrderReceiveKindEnum(str, Enum):
    take_home = "take_home"
    take_away = "take_away"


class OrderRespDTO(BaseModel):
    id: int = Field(title="Идентификатор заказа")
    products: list[ProductRespDTO] = Field(title="Список добавленных продуктов")
    status: OrderStatusEnum = Field(title="Статус заказа")
    created_at: datetime = Field(title="Дата создания")
    receive_kind: OrderReceiveKindEnum = Field(title="Способ доставки")
    summ: float = Field(title="Общая сумма заказа")


class OrderListRespDTO(BaseModel):
    order: list[OrderRespDTO] = Field(title="Состав заказа")
    total: int = Field(title="Общее кол-во заказов")
