from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    DateTime,
    Boolean,
    Date,
)
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now

from app.base.models import BaseModel

__all__ = ("UserModel", )


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, Identity(), primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=now())
    is_active = Column(Boolean, nullable=False, server_default=expression.false())
    name = Column(Text, nullable=True)
    birthday = Column(Date, nullable=True)
