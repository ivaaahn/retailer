from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.base.deps import BasePagingParams
from app.dto.api.products import ShopProductDTO
from app.dto.api.profile import AddressRespDTO
from app.models.orders import OrderReceiveKindEnum, OrderStatusEnum
from pydantic import BaseModel, Field


class OrderListSortByEnum(str, Enum):
    id = "id"
    created_at = "created_at"


@dataclass
class OrderListPagingParams(BasePagingParams):
    sort_by: OrderListSortByEnum


class OrderBaseDTO(BaseModel):
    id: int = Field(title="Идентификатор заказа")
    status: OrderStatusEnum = Field(title="Статус заказа")
    created_at: datetime = Field(title="Дата создания")
    receive_kind: OrderReceiveKindEnum = Field(title="Способ получения")
    delivery_address: int | None = Field(
        title="Адрес доставки (если выбрана доставка)"
    )
    total_price: float = Field(title="Общая стоимость заказа")


# TODO доделать адрес
class OrderRespDTO(OrderBaseDTO):
    products: list[ShopProductDTO] = Field(
        title="Список добавленных продуктов"
    )
    delivery_address: AddressRespDTO | None = Field(title="Адрес доставки")


class OrdersListRespDTO(BaseModel):
    orders: list[OrderBaseDTO] = Field(title="Список заказов")
    total: int = Field(title="Общее кол-во заказов")


class PlaceOrderReqDTO(BaseModel):
    shop_id: int = Field(title="Идентификатор магазина")
    receive_kind: OrderReceiveKindEnum = Field(
        title="Способ получения", default=OrderReceiveKindEnum.takeaway
    )
    delivery_address_id: int | None = Field(
        title="Адрес доставки (если выбрана доставка)", default=None
    )


class PlaceOrderRespDTO(BaseModel):
    order_id: int
