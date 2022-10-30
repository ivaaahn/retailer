from functools import lru_cache

from config import RetailerConfig


class ProductsServiceConfig(RetailerConfig):
    use_cache: bool = False

    class Config:
        env_prefix = "PRODUCTS_SERVICE_"


@lru_cache
def get_config():
    return ProductsServiceConfig()
