from enum import Enum

from aiobotocore.client import AioBaseClient
from aiobotocore.session import get_session, AioSession

from ..base.accessor import BaseAccessor
from .settings import S3Settings, get_settings


class ACLTypeEnum(str, Enum):
    private = "private"
    public_read = "public_read"
    public_read_write = "public_read_write"


class S3Accessor(BaseAccessor[S3Settings]):
    class Meta:
        name = "S3"

    def __init__(self, settings: S3Settings):
        super().__init__(settings)

        self._session = get_session()
        self._client_ctx = None
        self._client = None

    @property
    def session(self) -> AioSession:
        return self._session

    @property
    def client(self) -> AioBaseClient:
        return self._client

    async def _connect(self):
        self._client_ctx = self.session.create_client(
            verify=False,
            service_name="s3",
            endpoint_url=self.conf.endpoint_url,
            region_name=self.conf.region,
            aws_secret_access_key=self.conf.secret_access_key,
            aws_access_key_id=self.conf.access_key_id,
        )
        self._client = await self._client_ctx.__aenter__()

    async def _disconnect(self):
        await self._client_ctx.__aexit__(None, None, None)
        self._client_ctx = None
        self._client = None


s3_accessor = S3Accessor(get_settings())