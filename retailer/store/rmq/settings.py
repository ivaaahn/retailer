from functools import lru_cache

from pydantic import BaseSettings


class RMQSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    queue_name: str

    class Config:
        env_file = "app.env"
        env_prefix = "RMQ_"


_settings = RMQSettings()


@lru_cache
def get_settings():
    return _settings
