from sqlalchemy import (
    Column,
    Integer,
    ForeignKey, Identity,
)

from app.base.models import BaseModel

__all__ = ("StaffModel",)


class StaffModel(BaseModel):
    __tablename__ = "staff"

    id = Column(Integer, Identity(), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), primary_key=True)
