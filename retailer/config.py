import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(
    BASE_DIR, os.environ.get("CONFIG_PATH", "etc/.env.local")
)


class RetailerConfig(BaseSettings):
    class Config:
        env_file = CONFIG_PATH
