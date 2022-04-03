from typing import Optional

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncEngine

from app.core.settings import PgSettings, get_settings
from store.base.accessor import BaseAccessor
from store.pg import sa


# TODO выделить базовый класс
class PgAccessor(BaseAccessor[PgSettings]):
    class Meta:
        name = "Postgres"

    def __init__(self, settings: PgSettings = Depends(get_settings)):
        super().__init__(settings)

        self._engine: Optional[AsyncEngine] = None
        self._metadata: Optional[MetaData] = None

    async def acquire(self) -> AsyncConnection:
        async with self._engine.begin() as conn:
            yield conn

    @property
    def meta(self) -> MetaData:
        return self._metadata

    async def _connect(self):
        conf = self._config

        try:
            self._engine = create_async_engine(
                url=conf.dsn,
                echo=conf.echo,
            )

            self._metadata = sa.metadata
            self._metadata.bind = self._engine  # TODO проверить обязательность

            return self
        except Exception as err:
            # TODO добавить logger
            raise err
