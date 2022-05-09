from functools import lru_cache

from pydantic import PostgresDsn

from config import RetailerConfig


class PgConfig(RetailerConfig):
    dsn: PostgresDsn
    echo: bool

    class Config:
        env_prefix = "PG_"


@lru_cache
def get_config() -> PgConfig:
    return PgConfig()
