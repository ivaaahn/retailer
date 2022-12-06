from functools import lru_cache

from retailer.config import RetailerConfig


class RMQConfig(RetailerConfig):
    host: str = "fixme"
    port: int = 8888
    user: str = "fixme"
    password: str = "fixme"
    queue_name: str = "fixme"
    on: bool = False

    class Config:
        env_prefix = "RMQ_"


@lru_cache
def get_config():
    return RMQConfig()
