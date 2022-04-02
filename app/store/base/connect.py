from typing import Generic, TypeVar

_Settings = TypeVar("_Settings")


class BaseConnect(Generic[_Settings]):
    class Meta:
        name = "Base"

    def __init__(self, settings: _Settings):
        self._config = settings
        self._name = self.Meta.name or self.__class__.__name__

    @property
    def conf(self) -> _Settings:
        return self._config

    async def _connect(self):
        pass

    async def _disconnect(self):
        pass

    async def connect(self):
        await self._connect()
        print(f"Connected to '{self._name}'")

    async def disconnect(self):
        await self._disconnect()
        print(f"Disconnected from '{self._name}'")
