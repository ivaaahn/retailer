import abc

__all__ = ("IAttachmentsRepo",)

from typing import Optional

from store.s3 import ACLTypeEnum


class IAttachmentsRepo(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def upload_bucket(
        self,
        body: bytes,
        content_type: str,
        acl: ACLTypeEnum = ACLTypeEnum.private,
    ) -> str:
        pass

    @abc.abstractmethod
    async def download_object(self, key: str):
        pass

    @abc.abstractmethod
    async def insert(self, name: str):
        pass
