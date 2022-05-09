from functools import lru_cache

from fastapi import Depends
from starlette.responses import StreamingResponse

from app.base.services import BaseService
from app.repos.attachments import IAttachmentsRepo
from app.repos.attachments.implementation import AttachmentsRepo

__all__ = ("AttachmentsService",)


@lru_cache
class AttachmentsService(BaseService):
    def __init__(
        self,
        attachments_repo: IAttachmentsRepo = Depends(AttachmentsRepo),
    ):
        super().__init__()
        self._attachments_repo = attachments_repo

    @staticmethod
    def make_s3_url(path: str) -> str:
        return f"/img/{path}"

    async def download_from_s3(self, key: str) -> StreamingResponse:
        return await self._attachments_repo.download_object(key)
