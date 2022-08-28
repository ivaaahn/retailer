import json

from aio_pika import Channel, Connection, Message, Queue, connect

from .config import RMQConfig, get_config
from ..base.accessor import BaseAccessor

__all__ = ("RMQAccessor", "rmq_accessor")


class RMQAccessor(BaseAccessor[RMQConfig]):
    class Meta:
        name = "RabbitMQ"

    def __init__(self, config: RMQConfig):
        super().__init__(config)
        self._connection: Connection | None = None
        self._channel: Channel | None = None
        self._queue: Queue | None = None

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


rmq_accessor = RMQAccessor(get_config())
