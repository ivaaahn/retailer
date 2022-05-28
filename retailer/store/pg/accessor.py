from typing import Optional

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from . import sa
from .config import PgConfig, get_config
from ..base.accessor import BaseAccessor

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
        # self._conn: Optional[AsyncConnection] = None

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

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
            echo_pool="debug",
            pool_size=8,
        )

        self._metadata = sa.metadata
        self._metadata.bind = self._engine  # TODO проверить обязательность

        return self

    async def _disconnect(self):
        await self.engine.dispose()


pg_accessor = PgAccessor(get_config())
