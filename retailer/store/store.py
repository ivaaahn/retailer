from functools import lru_cache
from typing import Iterable, TYPE_CHECKING

from app.core.settings import Settings, get_settings
from .pg.accessor import PgAccessor
from .rmq import RMQAccessor

if TYPE_CHECKING:
    from core.settings import Settings
    from .base.accessor import BaseAccessor


class AppStore:
    def __init__(self, settings: "Settings"):
        self.pg = PgAccessor(settings.pg)
        self.rmq = RMQAccessor(settings.rmq)

    def _accessors(self) -> Iterable["BaseAccessor"]:
        yield self.pg
        yield self.rmq

    async def connect(self):
        for accessor in self._accessors():
            await accessor.connect()

    async def disconnect(self):
        for accessor in self._accessors():
            await accessor.disconnect()


_store = AppStore(get_settings())


@lru_cache
def get_store():
    return _store
