from typing import TYPE_CHECKING

from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection

from store.rmq import RMQAccessor
from store.store import Store

if TYPE_CHECKING:
    from store.pg.accessor import PgAccessor


class BaseRepo:
    pass


class BaseRMQRepo(BaseRepo):
    def __init__(self):
        self._rmq: "RMQAccessor" = Store.rmq


class BasePgRepo(BaseRepo):
    def __init__(self):
        self._pg: "PgAccessor" = Store.pg

    async def execute(
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
