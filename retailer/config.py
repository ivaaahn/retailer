import os
from enum import Enum

from pydantic import BaseSettings


class EnvKinds(str, Enum):
    PROD = "prod"
    LOCAL = "local"
    TESTS_CI = "tests_ci"
    TESTS_LOCAL = "tests_local"


RUN_MODE = EnvKinds(os.environ.get("RUN_MODE", "local"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


dotenv_files: dict[EnvKinds, str] = {
    kind: os.path.join(BASE_DIR, "etc", f".env.{kind}") for kind in EnvKinds
}


class RetailerConfig(BaseSettings):
    class Config:
        env_file = dotenv_files[RUN_MODE]
