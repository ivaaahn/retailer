from typing import Generic, TypeVar

from logger import get_logger

_Settings = TypeVar("_Settings")


class BaseAccessor(Generic[_Settings]):
    class Meta:
        name = "Base"

    def __init__(self, settings: _Settings):
        self._config = settings
        self._name = self.Meta.name or self.__class__.__name__
        self._connected: bool = False
        self._logger = get_logger(self._name)

    @property
    def conf(self) -> _Settings:
        return self._config

    async def _connect(self):
        pass

    async def _disconnect(self):
        pass

    async def connect(self):
        if not self._connected:
            await self._connect()
            self._connected = True

            self._logger.info(f"Connected to '{self._name}'")

    async def disconnect(self):
        if self._connected:
            await self._disconnect()
            self._connected = False
            self._logger.info(f"Disconnected from '{self._name}'")

    async def __call__(self):
        await self.connect()
        return self
