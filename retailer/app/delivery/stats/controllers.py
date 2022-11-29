from datetime import date

from app.base.errors import ForbiddenError
from app.delivery.auth.deps import get_current_active_user
from app.dto.api.stats import StatRespDTO
from app.dto.api.user import UserRespDTO
from app.services.stats.service import StatsService
from fastapi import APIRouter, Depends, Query

router = APIRouter(
    prefix="/stats",
    tags=["analytics"],
)


@router.get("", response_model=StatRespDTO)
async def get_stat(
    count: int = Query(..., title="Количество магазинов"),
    date_from: date = Query(..., title="Дата начала периода"),
    date_to: date = Query(..., title="Дата окончания периода"),
    stat_service: StatsService = Depends(),
    user: UserRespDTO = Depends(get_current_active_user),
) -> StatRespDTO:
    if not user.is_manager:
        raise ForbiddenError

    return await stat_service.get_stat(count, date_from, date_to)
