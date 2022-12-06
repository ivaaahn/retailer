import asyncio

from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import text

from retailer.store import pg_accessor

from ..app.application import app
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
def event_loop():
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def cli() -> AsyncClient:
    async with AsyncClient(
        app=app, base_url="http://test"
    ) as client, LifespanManager(app):
        yield client


@pytest.fixture(scope="session")
async def db():
    accessor = pg_accessor()
    await accessor.connect()
    # conn = await accessor.engine.connect()
    # ctx = accessor.engine.begin()
    # conn = await ctx.start()
    yield accessor.engine
    # await ctx.transaction.rollback()
    await clear_db()


async def clear_db():
    accessor = pg_accessor()
    await accessor.connect()

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
