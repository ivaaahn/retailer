import abc

from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import DBOrderProductsDTO, DBOrderProductsListDTO

__all__ = ("IOrdersRepo",)


class IOrdersRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, id: int) -> DBOrderProductsDTO:
        pass

    @abc.abstractmethod
    async def get_list(
        self, paging_params: OrderListPagingParams
    ) -> DBOrderProductsListDTO:
        pass
