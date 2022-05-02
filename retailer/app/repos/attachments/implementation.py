import uuid
from functools import lru_cache

from aiobotocore.client import AioBaseClient
from fastapi.responses import StreamingResponse

from app.base.repo import BaseS3Repo
from app.delivery.attachments.errors import AttachmentNotFound
from app.repos.attachments import IAttachmentsRepo
from store.s3.accessor import ACLTypeEnum

__all__ = ("AttachmentsRepo",)


@lru_cache
class AttachmentsRepo(IAttachmentsRepo, BaseS3Repo):
    chunk_size = 69 * 1024

    @staticmethod
    def _gen_key() -> str:
        return uuid.uuid4().hex

    @property
    def s3_client(self) -> AioBaseClient:
        return self._s3.client

    async def upload_bucket(
        self,
        body: bytes,
        content_type: str,
        acl: ACLTypeEnum = ACLTypeEnum.private,
    ) -> str:
        key = self._gen_key()
        await self.s3_client.put_object(
            Bucket=self._s3.conf.bucket,
            Key=key,
            Body=body,
            ACL=acl.name,
            ContentType=content_type,
        )

        return key

    async def download_object(self, key: str) -> StreamingResponse:
        try:
            s3_object = await self.s3_client.get_object(
                Bucket=self._s3.conf.bucket,
                Key=key,
            )
        except Exception:
            raise AttachmentNotFound(key)

        # resp.content_type = object_info["content-type"]
        # resp.content_length = object_info["content-length"]

        object_info = s3_object["ResponseMetadata"]["HTTPHeaders"]

        return StreamingResponse(
            s3_object["Body"],
            headers={
                "Content-Disposition": f"attachment; filename='{key.split('/')[-1]}'",
                "Content-Type": object_info["content-type"],
            },
            media_type=object_info["content-type"],
        )

    async def insert(self, name: str):
        pass
