from fastapi import FastAPI

from core.routes import setup_routes
from store import Store

app = FastAPI()


@app.on_event("startup")
async def init_app():
    setup_routes(app)
    await Store.connect()


@app.on_event("shutdown")
async def stop_app():
    await Store.disconnect()
