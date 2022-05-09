from pydantic import BaseSettings

from config import RetailerConfig


class LoggerConfig(RetailerConfig):
    base_level: str
    log_format: str
    stderr_logger: bool
    stderr_logger_level: str
    file_logger: bool
    file_logger_level: str
    file_logger_filename: str

    class Config:
        env_prefix = "LOG_"


_config = LoggerConfig()


def get_config() -> LoggerConfig:
    return _config
