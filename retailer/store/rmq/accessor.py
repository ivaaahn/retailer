import json
from typing import Optional

from aio_pika import connect, Connection, Channel, Message, Queue

from ..base.accessor import BaseAccessor
from .settings import get_settings, RMQSettings

__all__ = ("RMQAccessor", "rmq_accessor")


class RMQAccessor(BaseAccessor[RMQSettings]):
    class Meta:
        name = "RabbitMQ"

    def __init__(self, settings: RMQSettings):
        super().__init__(settings)
        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None
        self._queue: Optional[Queue] = None

    async def _connect(self):
        self._connection = await connect(
            host=self.conf.host,
            port=self.conf.port,
            login=self.conf.user,
            password=self.conf.password,
        )
        self._channel = await self._connection.channel()
        self._queue = await self._channel.declare_queue(
            name=self.conf.queue_name, durable=True
        )

    async def _disconnect(self):
        if self._connection:
            await self._connection.close()

    async def send(self, message: dict):
        await self._channel.default_exchange.publish(
            message=Message(json.dumps(message).encode()),
            routing_key=self._queue.name,
        )


rmq_accessor = RMQAccessor(get_settings())
