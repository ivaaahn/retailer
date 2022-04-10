from .pg import pg_accessor
from .rmq import rmq_accessor


async def shutdown_store():
    await pg_accessor.disconnect()
    await rmq_accessor.disconnect()
