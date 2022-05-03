from functools import lru_cache

from config import RetailerSettings


class RMQSettings(RetailerSettings):
    host: str
    port: int
    user: str
    password: str
    queue_name: str

    class Config:
        env_prefix = "RMQ_"


_settings = RMQSettings()


@lru_cache
def get_settings():
    return _settings
