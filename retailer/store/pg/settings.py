from functools import lru_cache

from pydantic import PostgresDsn, BaseSettings


class PgSettings(BaseSettings):
    dsn: PostgresDsn
    echo: bool

    class Config:
        env_file = ".env"
        env_prefix = "PG_"


_settings = PgSettings()


@lru_cache
def get_settings():
    return _settings
