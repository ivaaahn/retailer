from pydantic import BaseSettings, PostgresDsn


class PgSettings(BaseSettings):
    dsn: PostgresDsn
    echo: bool

    class Config:
        env_prefix = "PG_"
        env_file = ".env"
