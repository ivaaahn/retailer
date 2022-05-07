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


@lru_cache
def get_config():
    return RMQConfig()
