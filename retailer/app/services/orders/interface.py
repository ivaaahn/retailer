from abc import ABC, abstractmethod

from app.dto.api.cart import CartRespDTO
from app.dto.api.orders import OrderListPagingParams
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
)
from app.models.orders import OrderReceiveKindEnum


class IOrdersRepo(ABC):
    @abstractmethod
    async def get(self, order_id: int) -> DBOrderProductsDTO:
        pass

    @abstractmethod
    async def get_list(
        self, user_id: int, paging_params: OrderListPagingParams
    ) -> DBOrderProductsListDTO:
        pass

    @abstractmethod
    async def create(
        self,
        user_id: int,
        shop_id: int,
        address_id: int,
        receive_kind: OrderReceiveKindEnum,
        cart: CartRespDTO,
    ) -> int:
        pass
