import os

from pydantic import BaseSettings

RUN_MODE = os.environ.get("RUN_MODE", "local")

dotenv_files = {
    "deploy": ".env.deploy",
    "test": ".env.test",
    "local": ".env.local",
}


class RetailerConfig(BaseSettings):
    class Config:
        env_file = dotenv_files[RUN_MODE]

