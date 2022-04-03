from fastapi import Depends
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from store.rmq import RMQAccessor
from store import get_store, AppStore


class BaseRepo:
    pass


class BaseRMQRepo(BaseRepo):
    def __init__(self, store: AppStore = Depends(get_store)):
        self._rmq: "RMQAccessor" = store.rmq


class BasePgRepo(BaseRepo):
    def __init__(self, store: AppStore = Depends(get_store)):
        self._pg = store.pg

    async def _execute(
        self,
        statement,
        parameters=None,
        debug: bool = False,
        **kwargs,
    ) -> CursorResult:
        if debug:
            print(
                f"{'='*44}[PG_REQUEST]{'='*44}\n" f"{str(statement)}\n" f"{'='*100}\n"
            )  # TODO logger
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
