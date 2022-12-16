import asyncio

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import text

from retailer.app.application import app
from retailer.app.urls import setup_routes
from retailer.store import pg_accessor, redis_accessor

from .fixtures import *  # noqa
from .mocks import *


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_app_routes():
    setup_routes(app)


@pytest.fixture
async def cli() -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def rabbit_cli(rmq_store: RMQAccessor):
    await rmq_store.delete_queue()
    await rmq_store.connect()
    yield rmq_store
    await rmq_store.delete_queue()
    await rmq_store.disconnect()


@pytest.fixture(scope="function")
async def engine():
    accessor = pg_accessor()
    await accessor.connect()
    await clear_db(accessor)
    yield accessor.engine
    await clear_db(accessor)
    await accessor.disconnect()


@pytest.fixture(scope="function")
async def redis_cli():
    accessor = redis_accessor()
    await accessor.connect()
    await accessor.cli.flushdb()
    yield accessor.cli
    await accessor.cli.flushdb()
    await accessor.disconnect()


async def clear_db(accessor: PgAccessor):
    for table in accessor.meta.sorted_tables:
        async with accessor.engine.begin() as conn:
            await conn.execute(text(f"TRUNCATE {table.name} CASCADE"))
            try:
                await conn.execute(
                    text(f"ALTER SEQUENCE {table.name}_id_seq RESTART WITH 1")
                )
            except:
                pass


@pytest.fixture
def make_s3_url_mocked(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(
        target="retailer.app.misc.make_s3_url",
        return_value=DEFAULT_S3_URL,
    )
