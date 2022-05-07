from typing import Optional

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncEngine

from ..base.accessor import BaseAccessor
from .config import PgConfig, get_config
from . import sa

__all__ = (
    "PgAccessor",
    "pg_accessor",
)


class PgAccessor(BaseAccessor[PgConfig]):
    class Meta:
        name = "Postgres"

    def __init__(self, config: PgConfig):
        super().__init__(config)

        self._engine: Optional[AsyncEngine] = None
        self._metadata: Optional[MetaData] = None

    async def acquire(self) -> AsyncConnection:
        async with self._engine.begin() as conn:
            yield conn

    async def _ping(self):
        async with self._engine.begin() as conn:
            await conn.execute(text("SELECT 2+2;"))

    @property
    def meta(self) -> MetaData:
        return self._metadata

    async def _connect(self):
        conf = self._config

        self._engine = create_async_engine(
            url=conf.dsn,
            echo=conf.echo,
        )

        self._metadata = sa.metadata
        self._metadata.bind = self._engine  # TODO проверить обязательность

        return self


pg_accessor = PgAccessor(get_config())
