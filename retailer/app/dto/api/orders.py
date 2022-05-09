from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.base.deps import BasePagingParams
from app.dto.api.products import ShopProductDTO
from app.models.orders import OrderStatusEnum, OrderReceiveKindEnum


class OrderListSortByEnum(str, Enum):
    id = "id"
    created_at = "created_at"


@dataclass
class OrderListPagingParams(BasePagingParams):
    sort_by: OrderListSortByEnum


class OrderRespDTO(BaseModel):
    id: int = Field(title="Идентификатор заказа")
    products: list[ShopProductDTO] = Field(title="Список добавленных продуктов")
    status: OrderStatusEnum = Field(title="Статус заказа")
    created_at: datetime = Field(title="Дата создания")
    receive_kind: OrderReceiveKindEnum = Field(title="Способ получения")
    total_price: float = Field(title="Общая стоимость заказа")


class OrdersListRespDTO(BaseModel):
    orders: list[OrderRespDTO] = Field(title="Список заказов")
    total: int = Field(title="Общее кол-во заказов")


class PlaceOrderRespDTO(BaseModel):
    order_id: int
