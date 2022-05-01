from functools import lru_cache

from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    secret: str
    alg: str
    access_token_exp_minutes: int

    class Config:
        env_file = "app.env"
        env_prefix = "AUTH_"


@lru_cache
def get_settings():
    return AuthSettings()
