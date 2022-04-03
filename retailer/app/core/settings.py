from functools import lru_cache

from pydantic import BaseSettings, PostgresDsn, AmqpDsn


class PgSettings(BaseSettings):
    dsn: PostgresDsn
    echo: bool

    class Config:
        env_prefix = "PG_"
        env_file = ".env"


class RMQSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    queue_name: str
    # reconnect_timeout: int = 5
    # capacity: int = 10

    class Config:
        env_file = ".env"
        env_prefix = "RMQ_"


# to get a string like this run:
# openssl rand -hex 32
class AuthSettings(BaseSettings):
    secret: str
    alg: str
    access_token_exp_minutes: int

    class Config:
        env_prefix = "AUTH_"
        env_file = ".env"


class Settings(BaseSettings):
    pg: PgSettings = PgSettings()
    rmq: RMQSettings = RMQSettings()
    auth: AuthSettings = AuthSettings()

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
