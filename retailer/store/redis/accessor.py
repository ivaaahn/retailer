from functools import lru_cache
from typing import Optional

from aioredis import Redis, from_url

from ..base.accessor import BaseAccessor
from .config import RedisConfig, get_config

__all__ = (
    "RedisAccessor",
    "redis_accessor",
)


class RedisAccessor(BaseAccessor[RedisConfig]):
    class Meta:
        name = "Redis"

    def __init__(self, config: RedisConfig):
        super().__init__(config)
        self._redis: Redis | None = None

    async def _ping(self):
        await self._redis.ping()

    async def _connect(self):
        self._redis = from_url(
            self.conf.dsn,
            encoding="utf-8",
            decode_responses=True,
        )

    async def _disconnect(self):
        if self._redis.connection:
            await self._redis.connection.disconnect()

    @property
    def cli(self) -> Redis:
        return self._redis


@lru_cache
def redis_accessor() -> RedisAccessor:
    return RedisAccessor(get_config())
