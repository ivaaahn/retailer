from functools import lru_cache

from config import RetailerConfig
from pydantic import RedisDsn


class RedisConfig(RetailerConfig):
    dsn: RedisDsn
    echo: bool

    class Config:
        env_prefix = "REDIS_"


@lru_cache
def get_config():
    return RedisConfig()
