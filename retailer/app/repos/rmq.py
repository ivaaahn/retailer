from dataclasses import asdict, dataclass

from app.base.repo import BaseRMQRepo


@dataclass(frozen=True, slots=True)
class MessageBody:
    title: str
    data: str
    description: str


@dataclass(frozen=True, slots=True)
class RMQMessage:
    subject: str
    recipients: list[str]
    formatted_body: MessageBody

    def to_dict(self) -> dict:
        return asdict(self)


class RMQInteractRepo(BaseRMQRepo):
    async def send_code(self, email: str, code: str):
        message = RMQMessage(
            subject="RetailerX: подтверждение регистрации",
            recipients=[email],
            formatted_body=MessageBody(
                title="Код подтверждения регистрации",
                data=code,
                description="В целях безопасности никому не сообщайте данный код!",
            ),
        )

        await self._rmq.send(message.to_dict())

    async def send_accept(self, email: str, order_id: int):
        message = RMQMessage(
            subject="RetailerX: подтверждение заказа",
            recipients=[email],
            formatted_body=MessageBody(
                title="Подтверждение оформления заказа",
                data=f"Заказ №{order_id}",
                description="Заказ оформлен и направлен в магазин",
            ),
        )
        await self._rmq.send(message.to_dict())
