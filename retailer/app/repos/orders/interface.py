import abc

from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.api.user import UserRespDTO
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
    async def create_order(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        total_price: float,
    ) -> int:
        pass

    @abc.abstractmethod
    async def fill_order_with_products(
        self,
        order_id: int,
        cart: CartRespDTO,
    ):
        pass
