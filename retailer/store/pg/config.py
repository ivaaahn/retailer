from functools import lru_cache

from config import RetailerConfig
from pydantic import PostgresDsn


class PgConfig(RetailerConfig):
    dsn: PostgresDsn
    dsn_alembic: PostgresDsn
    echo: bool
    echo_pool: bool | str = False
    pool_size: int = 8

    class Config:
        env_prefix = "PG_"


@lru_cache
def get_config() -> PgConfig:
    return PgConfig()
