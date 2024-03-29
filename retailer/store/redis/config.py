from functools import lru_cache

from config import RetailerConfig
from pydantic import RedisDsn


class RedisConfig(RetailerConfig):
    dsn: RedisDsn = "redis://FIXME@FIXME/FIXME"
    echo: bool = False

    class Config:
        env_prefix = "REDIS_"


@lru_cache
def get_config():
    return RedisConfig()
