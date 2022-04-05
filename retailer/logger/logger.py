import logging

from fastapi import Depends

from .settings import LoggerSettings, get_settings


class LoggerFactory:
    def __init__(self, settings: LoggerSettings):
        self._settings = settings

    @property
    def conf(self) -> LoggerSettings:
        return self._settings

    def _setup_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)

        logger.setLevel(self.conf.base_level)

        if self.conf.file_logger:
            self._add_file_handler(logger)

        if self.conf.stderr_logger:
            self._add_stderr_handler(logger)

        return logger

    def create(self, name: str) -> logging.Logger:
        new_logger = self._setup_logger(name)
        return new_logger

    def _add_file_handler(self, logger: logging.Logger):
        file_handler = logging.FileHandler(self.conf.file_logger_filename)
        file_handler.setLevel(self.conf.file_logger_level)
        file_handler.setFormatter(logging.Formatter(self.conf.log_format))

        logger.addHandler(file_handler)

    def _add_stderr_handler(self, logger: logging.Logger):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.conf.stderr_logger_level)
        stream_handler.setFormatter(logging.Formatter(self.conf.log_format))

        logger.addHandler(stream_handler)


_factory = LoggerFactory(get_settings())


def get_logger(name: str) -> logging.Logger:
    return _factory.create(name)
