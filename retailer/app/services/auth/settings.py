from functools import lru_cache


from config import RetailerSettings


class AuthSettings(RetailerSettings):
    secret: str
    alg: str
    access_token_exp_minutes: int

    class Config:
        env_prefix = "AUTH_"


@lru_cache
def get_settings():
    return AuthSettings()
