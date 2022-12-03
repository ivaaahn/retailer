import logging
from asyncio import gather

from fastapi import Depends
from logger.logger import get_logger
from sqlalchemy import asc, desc
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.orm import Query

from retailer.app.base.deps import SortOrderEnum
from retailer.store import redis_accessor
from retailer.store.pg import PgAccessor, pg_accessor
from retailer.store.redis import RedisAccessor
from retailer.store.rmq import RMQAccessor, rmq_accessor
from retailer.store.s3 import S3Accessor, s3_accessor


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
        self._rmq = rmq


class BaseS3Repo(BaseRepo):
    def __init__(self, s3: S3Accessor = Depends(s3_accessor)):
        super().__init__()
        self._s3 = s3


class BaseRedisRepo(BaseRepo):
    def __init__(self, redis: RedisAccessor = Depends(redis_accessor)):
        super().__init__()
        self._redis = redis


class BasePgRepo(BaseRepo):
    def __init__(self, pg: PgAccessor = Depends(pg_accessor)):
        super().__init__()
        self._pg = pg

    @property
    def engine(self) -> AsyncEngine:
        return self._pg.engine

    @staticmethod
    def with_pagination(
        query: Query, count: int, offset: int, order: SortOrderEnum, sort: any
    ) -> Query:
        query = query.limit(count)
        query = query.offset(offset)

        order_func = asc if order is SortOrderEnum.asc else desc

        query = query.order_by(order_func(sort))

        return query

    async def _gather_execute(self, *stmts):
        queries = [self._execute(stmt) for stmt in stmts]
        return await gather(*queries)

    async def _execute(
        self,
        statement,
        parameters=None,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> CursorResult:
        if conn:
            return await conn.execute(
                statement=statement,
                parameters=parameters,
                **kwargs,
            )

        async with self.engine.connect() as conn:
            res = await conn.execute(
                statement=statement,
                parameters=parameters,
                **kwargs,
            )

            await conn.commit()

        return res

    async def execute_with_pk(
        self,
        statement,
        parameters=None,
        conn: AsyncConnection | None = None,
        **kwargs,
    ) -> int:
        cursor = await self._execute(statement, parameters, conn, **kwargs)
        return cursor.inserted_primary_key[0]

    async def get_one(
        self,
        statement,
        parameters=None,
        conn: AsyncConnection | None = None,
        **kwargs,
    ):
        cursor = await self._execute(statement, parameters, conn, **kwargs)
        return cursor.first()

    async def get_scalar(
        self,
        statement,
        parameters=None,
        conn: AsyncConnection | None = None,
        **kwargs,
    ):
        cursor = await self._execute(statement, parameters, conn, **kwargs)
        return cursor.scalar()
