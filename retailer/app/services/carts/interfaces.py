from abc import ABC, abstractmethod

from retailer.app.dto.db.products import DBCartInfoDTO, DBCartProductDTO


class ICartsRepo(ABC):
    @abstractmethod
    async def add_to_cart(self, email: str, dto: DBCartProductDTO) -> int:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, email: str, product_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get(self, email: str) -> DBCartInfoDTO:
        raise NotImplementedError

    @abstractmethod
    async def clear_cart(self, email: str) -> int:
        raise NotImplementedError
