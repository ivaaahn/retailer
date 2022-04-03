from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now

from app.base.models import BaseModel


# TODO добавить на email индекс
class WebUsers(BaseModel):
    __tablename__ = "web_users"

    id = Column(Integer, Identity(), primary_key=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=now())
    is_active = Column(Boolean, nullable=False, server_default=expression.false())
