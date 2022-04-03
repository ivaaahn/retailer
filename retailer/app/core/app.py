from fastapi import FastAPI

from core.routes import setup_routes
from store import get_store

app = FastAPI()


@app.on_event("startup")
async def init_app():
    setup_routes(app)
    await get_store().connect()


@app.on_event("shutdown")
async def stop_app():
    await get_store().disconnect()
