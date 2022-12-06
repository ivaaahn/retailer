from logging import Logger
from typing import Generic, TypeVar

from retailer.logger import get_logger

_Config = TypeVar("_Config")


class BaseAccessor(Generic[_Config]):
    class Meta:
        name = "Base"

    def __init__(self, config: _Config):
        self._config = config
        self._name = self.Meta.name or self.__class__.__name__
        self._connected: bool = False
        self._logger = get_logger(self._name)

    @property
    def logger(self) -> Logger:
        return self._logger

    @property
    def conf(self) -> _Config:
        return self._config

    async def ping(self):
        if not self._connected:
            return

        self.logger.info(f"[~] Pinging {self._name}...")

        try:
            await self._ping()
        except Exception as err:
            self.logger.exception(str(err))
            raise err
        else:
            self.logger.info("[~] OK")

    async def connect(self):
        if self._connected:
            return

        self._logger.info(f"[...] Connecting to '{self._name}'")

        try:
            await self._connect()
        except Exception as err:
            self.logger.exception(str(err))
            raise err
        else:
            self._connected = True
            await self.ping()

        self._logger.info(f"[+] Connected to '{self._name}'")

    async def disconnect(self):
        if self._connected:
            await self._disconnect()
            self._connected = False
            self._logger.info(f"Disconnecting from '{self._name}'")

    async def __call__(self):
        await self.connect()
        return self

    async def _ping(self):
        self.logger.info("[*] SKIPPED")

    async def _connect(self):
        pass

    async def _disconnect(self):
        pass
