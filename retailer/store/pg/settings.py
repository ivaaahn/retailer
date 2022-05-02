from functools import lru_cache

from pydantic import PostgresDsn

from config import RetailerSettings


class PgSettings(RetailerSettings):
    dsn: PostgresDsn
    echo: bool

    class Config:
        env_prefix = "PG_"


_settings = PgSettings()


@lru_cache
def get_settings():
    return _settings
