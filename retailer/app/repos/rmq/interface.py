import abc


class IRMQInteractRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def send_code(self, email: str, code: str):
        pass

    @abc.abstractmethod
    async def send_accept(self, email: str, order_id: int):
        pass
