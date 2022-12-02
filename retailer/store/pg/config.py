from functools import lru_cache

from config import RetailerConfig
from pydantic import PostgresDsn


class PgConfig(RetailerConfig):
    dsn: PostgresDsn = "postgresql+asyncpg://FIXME:FIXME@FIXME:5432/FIXME"
    echo: bool = False
    on: bool = False
    echo_pool: bool | str = False
    pool_size: int = 8

    class Config:
        env_prefix = "PG_"


@lru_cache
def get_config() -> PgConfig:
    return PgConfig()
