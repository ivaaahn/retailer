from pydantic import BaseSettings


# to get a string like this run:
# openssl rand -hex 32
class AuthSettings(BaseSettings):
    secret: str
    alg: str
    access_token_exp_minutes: int

    class Config:
        env_prefix = "AUTH_"
        env_file = ".env"
