from functools import lru_cache

from pydantic import RedisDsn

from config import RetailerConfig


class RedisConfig(RetailerConfig):
    dsn: RedisDsn
    echo: bool

    class Config:
        env_prefix = "REDIS_"


@lru_cache
def get_config():
    return RedisConfig()
