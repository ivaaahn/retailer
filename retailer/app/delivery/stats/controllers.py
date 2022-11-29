from datetime import date

from app.dto.api.stats import StatRespDTO
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
) -> StatRespDTO:
    return await stat_service.get_stat(count, date_from, date_to)
