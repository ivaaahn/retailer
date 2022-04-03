import abc
from functools import lru_cache


@lru_cache
class IRMQInteractRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def send_code(self, email: str, code: str):
        pass
