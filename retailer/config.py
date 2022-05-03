import os

from pydantic import BaseSettings


DEPLOY_MODE = os.environ.get("DEPLOY_MODE", False)

dotenv_files = {
    "deploy": "deploy.env",
    "test": "test.env",
}


class RetailerSettings(BaseSettings):
    class Config:
        env_file = dotenv_files["deploy"] if DEPLOY_MODE else dotenv_files["test"]
