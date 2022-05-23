import logging

from fastapi import Depends
from sqlalchemy import asc, desc
from sqlalchemy.engine import CursorResult
from sqlalchemy.orm import Query

from app.base.deps import SortOrderEnum
from logger.logger import get_logger
from store import redis_accessor
from store.pg import pg_accessor, PgAccessor
from store.redis import RedisAccessor
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


class BaseRedisRepo(BaseRepo):
    def __init__(self, redis: RedisAccessor = Depends(redis_accessor)):
        super().__init__()
        self._redis = redis


class BasePgRepo(BaseRepo):
    def __init__(self, pg: PgAccessor = Depends(pg_accessor)):
        super().__init__()
        self._pg = pg

    @staticmethod
    def with_pagination(
        query: Query, count: int, offset: int, order: SortOrderEnum, sort: any
    ) -> Query:
        query = query.limit(count)
        query = query.offset(offset)

        order_func = asc if order is SortOrderEnum.asc else desc

        query = query.order_by(order_func(sort))

        return query

    async def _execute(
        self,
        statement,
        parameters=None,
        **kwargs,
    ) -> CursorResult:
        # self.logger.info(
        #     f"\n{'='*44}[PG_REQUEST]{'='*44}\n" f"{str(statement)}\n" f"{'='*100}\n"
        # )

        async with self._pg.acquire() as conn:
            result = await conn.execute(
                statement=statement,
                parameters=parameters,
                **kwargs,
            )

        return result

    async def execute_with_pk(self, statement, parameters=None, **kwargs) -> int:
        cursor = await self._execute(statement, parameters, **kwargs)
        return cursor.inserted_primary_key[0]

    async def get_one(self, statement, parameters=None, **kwargs):
        cursor = await self._execute(statement, parameters, **kwargs)
        return cursor.first()

    async def get_scalar(self, statement, parameters=None, **kwargs):
        cursor = await self._execute(statement, parameters, **kwargs)
        return cursor.scalar()
