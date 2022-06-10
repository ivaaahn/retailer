import abc

from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import DBOrderProductsDTO, DBOrderProductsListDTO
from app.models.orders import OrderReceiveKindEnum

__all__ = ("IOrdersRepo",)


class IOrdersRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, id: int) -> DBOrderProductsDTO:
        pass

    @abc.abstractmethod
    async def get_list(
        self, user_id: int, paging_params: OrderListPagingParams
    ) -> DBOrderProductsListDTO:
        pass

    @abc.abstractmethod
    async def create(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        cart: CartRespDTO,
    ) -> int:
        pass
