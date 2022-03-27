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

    def _connect(self):
        pass

    def connect(self):
        self._connect()
        print(f"Connected to '{self._name}'")
