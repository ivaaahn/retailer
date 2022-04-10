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
