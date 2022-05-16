from app.base.repo import BasePgRepo
from app.dto.db.orders import DBOrderProductsDTO
from app.repos.orders.interface import IOrdersRepo


class OrdersRepo(IOrdersRepo, BasePgRepo):
    async def get(self, id: int) -> DBOrderProductsDTO:
        pass
