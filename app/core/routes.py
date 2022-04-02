from typing import TYPE_CHECKING

from fastapi import APIRouter

import auth

if TYPE_CHECKING:
    from core.app import Application


router = APIRouter(
    prefix="/api",
    tags=["root"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)


def setup_routes(app: "Application"):
    router.include_router(auth.router)
    app.include_router(router)
