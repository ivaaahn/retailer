import logging

from fastapi import Depends
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from logger.logger import get_logger
from store.pg import pg_accessor, PgAccessor
from store.rmq import RMQAccessor, rmq_accessor
from store.s3 import S3Accessor, s3_accessor


class BaseRepo:
    class Meta:
        name = None

    def __init__(self):
        self._name = self.Meta.name or self.__class__.__name__
        self._logger = get_logger(self._name)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @property
    def name(self) -> str:
        return self._name


class BaseRMQRepo(BaseRepo):
    def __init__(self, rmq: RMQAccessor = Depends(rmq_accessor)):
        super().__init__()
        self._rmq: "RMQAccessor" = rmq


class BaseS3Repo(BaseRepo):
    def __init__(self, s3: S3Accessor = Depends(s3_accessor)):
        super().__init__()
        self._s3 = s3


class BasePgRepo(BaseRepo):
    def __init__(self, pg: PgAccessor = Depends(pg_accessor)):
        super().__init__()
        self._pg = pg

    async def _execute(
        self,
        statement,
        parameters=None,
        **kwargs,
    ) -> CursorResult:
        self.logger.info(
            f"\n{'='*44}[PG_REQUEST]{'='*44}\n" f"{str(statement)}\n" f"{'='*100}\n"
        )

        async with self._pg._engine.begin() as conn:
            conn: AsyncConnection

            result = await conn.execute(
                statement=statement,
                parameters=parameters,
                **kwargs,
            )

        return result

    @property
    def transaction(self) -> AsyncConnection:
        return self._pg._engine.begin()
