import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from retailer.store.pg.sa import metadata
from retailer.store.pg.settings import get_settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


###############DO NOT DELETE########################
from retailer.app.models.signup_session import *
from retailer.app.models.users import *
from retailer.app.models.shops import *
from retailer.app.models.products import *
from retailer.app.models.addresses import *
from retailer.app.models.product_categories import *
####################################################


# Parsing cfg .env with pg settings
pg_settings = get_settings()


alembic_config = context.config


def set_sqlalchemy_dsn(dsn: str):
    alembic_config.set_main_option(
        name="sqlalchemy.url",
        value=dsn,
    )


# Interpret the cfg file for Python logging.
# This line sets up loggers basically.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the cfg, defined by the needs of env.py,
# can be acquired:
# my_important_option = cfg.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context._execute() here emit the given string to the
    script output.
    """

    set_sqlalchemy_dsn(pg_settings.dsn)

    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    set_sqlalchemy_dsn(pg_settings.dsn)

    connectable = AsyncEngine(
        engine_from_config(
            alembic_config.get_section(alembic_config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
