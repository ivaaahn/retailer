import copy

from retailer.app.dto.db.products import DBShopProductDTO
from retailer.tests.builders.db.common import BaseBuilder


class DBProductBuilder(BaseBuilder):
    def __init__(self):
        self._id = 1
        self._name = "product name"
        self._photo = "https://fixme.com/fixme"
        self._description = "product description"
        self._category = "product category"
        self._price = 1000
        self._availability = 1000

    def but(self) -> "DBProductBuilder":
        return copy.deepcopy(self)

    def with_id(self, value: int) -> "DBProductBuilder":
        self._id = value
        return self

    def with_name(self, value: str) -> "DBProductBuilder":
        self._name = value
        return self

    def with_photo(self, value: str) -> "DBProductBuilder":
        self._photo = value
        return self

    def with_description(self, value: str) -> "DBProductBuilder":
        self._description = value
        return self

    def with_category(self, value: str) -> "DBProductBuilder":
        self._category = value
        return self

    def with_price(self, value: float) -> "DBProductBuilder":
        self._price = value
        return self

    def with_availability(self, value: int) -> "DBProductBuilder":
        self._availability = value
        return self

    def build(self) -> DBShopProductDTO:
        return DBShopProductDTO(
            id=self._id,
            name=self._name,
            photo=self._photo,
            description=self._description,
            category=self._category,
            price=self._price,
            availability=self._availability,
        )
