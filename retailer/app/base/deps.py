from fastapi import Depends
from pydantic import BaseModel, Field


class PagingQueryDTO(BaseModel):
    count: int = Field(title="Кол-во отображений")
    offset: int = Field(title="Смещение по записям")


# TODO допилить ошибку если что-то не указали
async def get_offset(q: PagingQueryDTO = Depends()):
    if q.offset and q.count:
        return PagingQueryDTO(count=q.count, offset=q.offset)
