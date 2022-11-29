from app.urls import setup_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from store import setup_store, shutdown_store

app = FastAPI(
    title="RetailerAPI",
    version="1.0.0",
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
    await setup_store()


@app.on_event("shutdown")
async def stop_app():
    await shutdown_store()
