from functools import lru_cache
from typing import Optional

from config import RetailerSettings


class S3Settings(RetailerSettings):
    endpoint_url: str
    secret_access_key: str
    access_key_id: str
    region: Optional[str] = None
    bucket: Optional[str] = None

    class Config:
        env_prefix = "S3_"


_settings = S3Settings()


@lru_cache
def get_settings():
    return _settings
