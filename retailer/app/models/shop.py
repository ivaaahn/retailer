from sqlalchemy import (
    Column,
    Integer,
    Identity,
    Text,
)

from app.base.models import BaseModel

__all__ = ("ShopModel",)


class ShopModel(BaseModel):
    __tablename__ = "shop"

    id = Column(Integer, Identity(), primary_key=True)
    city = Column(Text, nullable=False, index=True)
    street = Column(Text, nullable=False, index=True)
    house = Column(Text, nullable=False)
    floor = Column(Integer, nullable=True)

    def _as_dict(self) -> dict:
        return {
            "id": self.id,
            "city": self.city,
            "street": self.street,
            "house": self.house,
            "floor": self.floor,
        }
