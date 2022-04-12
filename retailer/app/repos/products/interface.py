import abc
from typing import Optional

from app.models.products import Products

__all__ = ("IProductsRepo",)


class IProductsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, name: str) -> Optional[Products]:
        pass
