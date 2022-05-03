from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.urls import setup_routes
from store import shutdown_store

app = FastAPI(
    title="RetailerAPI",
    version="0.1.11",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def init_app():
    setup_routes(app)
    # ping_store() # TODO


@app.on_event("shutdown")
async def stop_app():
    await shutdown_store()
