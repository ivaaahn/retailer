from base.repo import BaseRMQRepo


class RMQInteractRepo(BaseRMQRepo):
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
