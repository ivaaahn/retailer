import abc

from app.dto.db.products import DBCartInfoDTO, DBCartProductDTO


class ICartsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add_to_cart(self, email: str, dto: DBCartProductDTO) -> int:
        pass

    async def remove(self, email: str, product_id: int) -> int:
        pass

    async def get(self, email: str) -> DBCartInfoDTO:
        pass

    async def clear_cart(self, email: str) -> int:
        pass
