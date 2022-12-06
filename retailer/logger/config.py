from retailer.config import RetailerConfig


class LoggerConfig(RetailerConfig):
    base_level: str = "WARNING"
    log_format: str = "%(levelname)s:  \t  %(message)s [%(asctime)s | %(filename)s:%(lineno)d | %(name)s -> %(funcName)s()]"
    stderr_logger: bool = False
    stderr_logger_level: str = "WARNING"
    file_logger: bool = False
    file_logger_level: str = "WARNING"
    file_logger_filename: str = "logs.log"

    class Config:
        env_prefix = "LOG_"


def get_config() -> LoggerConfig:
    return LoggerConfig()
