from pydantic import BaseSettings


class LoggerSettings(BaseSettings):
    base_level: str
    log_format: str
    stderr_logger: bool
    stderr_logger_level: str
    file_logger: bool
    file_logger_level: str
    file_logger_filename: str

    class Config:
        env_file = "app.env"
        env_prefix = "LOG_"


_settings = LoggerSettings()


def get_settings() -> LoggerSettings:
    return _settings
