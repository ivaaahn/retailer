from enum import Enum
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    Identity,
    ForeignKey,
    Float,
    DateTime,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql.functions import now

from app.base.models import BaseModel

__all__ = (
    "OrderModel",
    "OrderReceiveKindEnum",
)


class OrderReceiveKindEnum(str, Enum):
    takeaway = "самовывоз"
    delivery = "доставка"


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
        server_default=OrderReceiveKindEnum.takeaway,
        nullable=False,
    )
    status = Column(
        ENUM(OrderStatusEnum, name="order_status_enum"),
        server_default=OrderStatusEnum.collecting,
        nullable=False,
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=now())

    def __init__(
        self, user: Optional[dict] = None, shop: Optional[dict] = None, **kwargs
    ):
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
