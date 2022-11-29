from .pg import PgAccessor, pg_accessor
from .redis import redis_accessor
from .rmq import rmq_accessor


def __accessors():
    yield pg_accessor()
    yield redis_accessor()
    yield rmq_accessor()


async def shutdown_store():
    for accessor in __accessors():
        await accessor.disconnect()


async def setup_store():
    for accessor in __accessors():
        await accessor.connect()
