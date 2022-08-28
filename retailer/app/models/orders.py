from enum import Enum
from typing import Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Identity, Integer
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql.functions import now

from app.base.models import BaseModel

__all__ = (
    "OrderModel",
    "OrderReceiveKindEnum",
)


class OrderReceiveKindEnum(str, Enum):
    takeaway = "takeaway"
    delivery = "delivery"


class OrderStatusEnum(str, Enum):
    collecting = "collecting"
    ready = "ready"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"
    finished = "finished"
    error = "error"


class OrderModel(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    total_price = Column(Float, nullable=False)
    receive_kind = Column(
        ENUM(OrderReceiveKindEnum, name="receive_kind_enum"),
        server_default=OrderReceiveKindEnum.takeaway.value,
        nullable=False,
    )
    status = Column(
        ENUM(OrderStatusEnum, name="order_status_enum"),
        server_default=OrderStatusEnum.collecting.value,
        nullable=False,
    )
    address_id = Column(Integer, ForeignKey("user_addresses.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=now())

    def __init__(self, user: dict | None = None, shop: dict | None = None, **kwargs):
        super().__init__(**kwargs)
        self._user = user
        self._shop = shop

    def _as_dict(self) -> dict:
        return {
            "id": self.id,
            "total_price": self.total_price,
            "receive_kind": self.receive_kind,
            "status": self.status,
            "created_at": self.created_at,
            "user": None,
            "shop": None,
        }

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def shop(self):
        return self._shop

    @shop.setter
    def shop(self, value):
        self._shop = value
