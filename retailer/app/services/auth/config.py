from functools import lru_cache


from config import RetailerConfig


class AuthConfig(RetailerConfig):
    secret: str
    alg: str
    access_token_exp_minutes: int

    class Config:
        env_prefix = "AUTH_"


@lru_cache
def get_config():
    return AuthConfig()
