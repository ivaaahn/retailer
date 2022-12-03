from datetime import date

from sqlalchemy import text
from sqlalchemy.engine import CursorResult

from retailer.app.base.repo import BasePgRepo
from retailer.app.dto.db.stats import DBStatOrdersDTO

__all__ = ("StatsRepo",)


class StatsRepo(BasePgRepo):
    async def get_stats(
        self, count: int, date_from: date, date_to: date
    ) -> list[DBStatOrdersDTO]:
        stmt = text("select * from order_stats(:count, :date_from, :date_to);")
        cursor: CursorResult = await self._execute(
            stmt, {"count": count, "date_from": date_from, "date_to": date_to}
        )

        return [
            DBStatOrdersDTO(
                shop_id=row["shop_id"],
                shop_orders_qty=row["shop_orders_qty"],
                shop_total_profit=row["shop_total_profit"],
                shop_address=row["shop_address"],
                client_name=row["client_name"],
                client_orders_qty=row["client_orders_qty"],
                client_spend=row["client_spend"],
            )
            for row in cursor
        ]
