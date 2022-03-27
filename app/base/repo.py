from typing import TYPE_CHECKING

from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.testing.plugin.plugin_base import util

from store.store import store

if TYPE_CHECKING:
    from store.pg.connect import PgConnect


class BaseRepo:
    pass


class BasePgRepo(BaseRepo):
    def __init__(self):
        self._pg: "PgConnect" = store.pg

    async def execute(
        self,
        statement,
        parameters=None,
        debug: bool = False,
        **kwargs,
    ) -> CursorResult:
        if debug:
            print("stmt: ", str(statement))  # TODO logger

        async with self._pg._engine.begin() as conn:
            conn: AsyncConnection

            result = await conn.execute(
                statement=statement,
                parameters=parameters,
                **kwargs,
            )

        return result
