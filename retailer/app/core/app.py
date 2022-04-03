from typing import Optional, TYPE_CHECKING, Iterable

from fastapi import FastAPI

from core.routes import setup_routes
from store.store import store
from .settings import Settings

if TYPE_CHECKING:
    from store.store import Store
    from store.base.connect import BaseConnect


def connections() -> Iterable["BaseConnect"]:
    yield store.pg
    yield store.rmq


async def make_connections():
    for conn in connections():
        await conn.connect()


async def disconnect():
    for conn in connections():
        await conn.disconnect()


app = FastAPI()

# TODO написать нормально
@app.on_event("startup")
async def init_app():
    setup_routes(app)
    await make_connections()


# TODO написать нормально
@app.on_event("shutdown")
async def init_app():
    await disconnect()
