from functools import lru_cache
from typing import Optional

from config import RetailerConfig


class S3Config(RetailerConfig):
    endpoint_url: str
    secret_access_key: str
    access_key_id: str
    region: Optional[str] = None
    bucket: Optional[str] = None

    class Config:
        env_prefix = "S3_"


@lru_cache
def get_config():
    return S3Config()
