from fastapi import APIRouter, FastAPI

from app.api.auth.controllers import router as auth_router
from app.api.profile.controllers import router as profile_router


router = APIRouter(
    prefix="/api",
    tags=["root"],
)


def setup_routes(app: FastAPI):
    router.include_router(auth_router)
    router.include_router(profile_router)
    app.include_router(router)
