import abc

from fastapi import Depends, Query

from app.delivery.auth.deps import get_current_active_user
from app.dto.api.orders import OrderListPagingParams
from app.dto.api.user import UserRespDTO
from app.dto.db.orders import (
    DBOrderProductsDTO,
    DBOrderProductsListDTO,
    DBPlaceOrderDTO,
)
from app.dto.db.products import DBCartInfoDTO
from app.models.orders import OrderReceiveKindEnum

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

    @abc.abstractmethod
    async def place_order(
        self,
        shop_id: int,
        cart: DBCartInfoDTO,
        email: str,
        receive_kind: OrderReceiveKindEnum = Query(
            default=OrderReceiveKindEnum.takeaway
        ),
    ) -> DBPlaceOrderDTO:
        pass
