from fastapi import APIRouter, FastAPI

from app.api.auth.controllers import router as auth_router


router = APIRouter(
    prefix="/api",
    tags=["root"],
)


def setup_routes(app: FastAPI):
    router.include_router(auth_router)
    app.include_router(router)
