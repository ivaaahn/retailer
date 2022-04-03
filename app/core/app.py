from typing import Optional, TYPE_CHECKING, Iterable

from fastapi import FastAPI

from core.routes import setup_routes
from store.store import store
from .settings import Settings

if TYPE_CHECKING:
    from store.store import Store
    from store.base.connect import BaseConnect


class Application(FastAPI):
    def __init__(self, settings: Settings, **kwargs):
        super().__init__(**kwargs)
        self._config = settings
        self._store: Optional["Store"] = None

    @property
    def conf(self) -> Settings:
        return self._config

    @staticmethod
    def _connections() -> Iterable["BaseConnect"]:
        yield store.pg
        yield store.rmq

    async def make_connections(self):
        for conn in self._connections():
            await conn.connect()

    async def disconnect(self):
        for conn in self._connections():
            await conn.disconnect()


app = Application(
    settings=Settings(),
    debug=True,
)


# TODO написать нормально
@app.on_event("startup")
async def init_app():
    setup_routes(app)
    await app.make_connections()


# TODO написать нормально
@app.on_event("shutdown")
async def init_app():
    await app.disconnect()
