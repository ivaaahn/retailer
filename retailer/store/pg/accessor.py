from functools import lru_cache

from sqlalchemy import MetaData, text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ..base.accessor import BaseAccessor
from . import sa
from .config import PgConfig, get_config

__all__ = (
    "PgAccessor",
    "pg_accessor",
)


class PgAccessor(BaseAccessor[PgConfig]):
    class Meta:
        name = "Postgres"

    def __init__(self, config: PgConfig):
        super().__init__(config)

        self._engine: AsyncEngine | None = None
        self._metadata: MetaData | None = None

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
        if not conf.on:
            return

        self._engine = create_async_engine(
            url=conf.dsn,
            echo=conf.echo,
            echo_pool=conf.echo_pool,
            pool_size=conf.pool_size,
        )

        self._metadata = sa.metadata
        self._metadata.bind = self._engine  # TODO проверить обязательность

        return self

    async def _disconnect(self):
        await self.engine.dispose()


@lru_cache
def pg_accessor() -> PgAccessor:
    return PgAccessor(get_config())
