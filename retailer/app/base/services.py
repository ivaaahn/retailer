import logging

from logger.logger import get_logger


class BaseService:
    class Meta:
        name = None

    def __init__(self):
        self._name = self.Meta.name or self.__class__.__name__
        self._logger = get_logger(self._name)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def name(self) -> str:
        return self._name
