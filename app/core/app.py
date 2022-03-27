from typing import Optional, TYPE_CHECKING, Iterable

from fastapi import FastAPI

from core.routes import setup_routes
from store.store import store
from .settings import Settings

if TYPE_CHECKING:
    from store import Store
    from store.base.connect import BaseConnect


class Application(FastAPI):
    def __init__(self, settings: Settings, **kwargs):
        super().__init__(**kwargs)
        self._config = settings
        self._store: Optional["Store"] = None

    @property
    def conf(self) -> Settings:
        return self._config

    # @property
    # def store(self) -> Optional["Store"]:
    #     return self._store

    # @store.setter
    # def store(self, value: "Store"):
    #     self._store = value
    #     print("Store is set")

    @staticmethod
    def _connections() -> Iterable["BaseConnect"]:
        yield store.pg

    async def make_connections(self):
        for conn in self._connections():
            conn.connect()


app = Application(
    settings=Settings(),
    debug=True,
)


# TODO написать нормально
@app.on_event("startup")
async def init_app():
    setup_routes(app)

    await app.make_connections()
    print(app)
