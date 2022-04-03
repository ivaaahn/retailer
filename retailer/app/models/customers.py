from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    ForeignKey,
    Date,
)

from app.base.models import BaseModel


class Customers(BaseModel):
    __tablename__ = "customers"

    id = Column(Integer, Identity(), primary_key=True)
    name = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("web_users.id"), nullable=False)
    birthday = Column(Date, nullable=True)
