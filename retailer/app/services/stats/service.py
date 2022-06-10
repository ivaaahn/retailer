from datetime import date
from functools import lru_cache

from fastapi import Depends

from app.base.services import BaseService
from app.dto.api.stats import StatEntityDTO, StatReqDTO, StatRespDTO
from app.repos.stat.implementation import StatsRepo

__all__ = ("StatsService",)


@lru_cache
class StatsService(BaseService):
    def __init__(
        self,
        stats_repo: StatsRepo = Depends(StatsRepo),
    ):
        super().__init__()
        self._stats_repo = stats_repo

    async def get_stat(self, count: int, date_from: date, date_to: date) -> StatRespDTO:
        try:
            res = await self._stats_repo.get_stats(count, date_from, date_to)
        except Exception as err:
            self.logger.exception(err)

        return StatRespDTO(
            best_shops=[
                StatEntityDTO(
                    shop_id=e.shop_id,
                    shop_orders_qty=e.shop_orders_qty,
                    shop_total_profit=e.shop_total_profit,
                    shop_address=e.shop_address,
                    client_name=e.client_name,
                    client_orders_qty=e.client_orders_qty,
                    client_spend=e.client_spend,
                )
                for e in res
            ]
        )
