from functools import lru_cache

from config import RetailerConfig


class RMQConfig(RetailerConfig):
    host: str
    port: int
    user: str
    password: str
    queue_name: str

    class Config:
        env_prefix = "RMQ_"


_config = RMQConfig()


@lru_cache
def get_config():
    return _config
