from functools import lru_cache

from app.base.repo import BaseRMQRepo
from .interface import IRMQInteractRepo


@lru_cache
class RMQInteractRepo(IRMQInteractRepo, BaseRMQRepo):
    async def send_code(self, email: str, code: str):
        await self._rmq.send(
            message={
                "subject": "Код подтверждения",
                "recipients": [email],
                "formatted_body": {
                    "title": "Код подтверждения регистрации",
                    "data": code,
                    "description": "В целях безопасности никому не сообщайте данный код!",
                },
            }
        )

    async def send_accept(self, email: str, order_id: int):
        await self._rmq.send(
            message={
                "subject": "Подтверждение заказа",
                "recipients": [email],
                "formatted_body": {
                    "title": f"Подтверждение оформления заказа",
                    "data": f"Заказ №{order_id}",
                    "description": "Заказ оформлен и направлен в магазин",
                },
            }
        )
