from functools import lru_cache

from pydantic import BaseSettings

from auth.user.settings import AuthSettings
from store.pg.settings import PgSettings


class Settings(BaseSettings):
    pg: PgSettings = PgSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
