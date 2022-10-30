from functools import lru_cache

from config import RetailerConfig


class AuthConfig(RetailerConfig):
    secret: str = "fixme"
    alg: str = "HS256"
    access_token_exp_minutes: int = 1440

    class Config:
        env_prefix = "AUTH_"


@lru_cache
def get_config():
    return AuthConfig()
