from fastapi import FastAPI

from app.urls import setup_routes
from store import shutdown_store

app = FastAPI()


@app.on_event("startup")
async def init_app():
    setup_routes(app)


@app.on_event("shutdown")
async def stop_app():
    await shutdown_store()
