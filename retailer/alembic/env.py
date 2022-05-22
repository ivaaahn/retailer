import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from app.models.order_products import *  # noqa
from app.models.orders import *  # noqa
from app.models.product_categories import *  # noqa
from app.models.products import *  # noqa
from app.models.shop_addresses import *  # noqa
from app.models.shop_products import *  # noqa
from app.models.shops import *  # noqa
from app.models.signup_sessions import *  # noqa
from app.models.staff import *  # noqa
from app.models.user_addresses import *  # noqa
from app.models.users import *  # noqa
from store.pg.config import get_config
from store.pg.sa import metadata

pg_config = get_config()


alembic_config = context.config


def set_sqlalchemy_dsn(dsn: str):
    alembic_config.set_main_option(
        name="sqlalchemy.url",
        value=dsn,
    )


def include_object(object, name, type_, reflected, compare_to):
    return not (type_ == "table" and reflected and compare_to is None)


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

    Calls to context.execute() here emit the given string to the
    script output.
    """

    set_sqlalchemy_dsn(pg_config.dsn)

    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    set_sqlalchemy_dsn(pg_config.dsn)

    connectable = AsyncEngine(
        engine_from_config(
            alembic_config.get_section(alembic_config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # target_metadata.reflect(, only=[
    #     "django_content_type",
    #     "auth_group",
    #     "auth_group_permisssions",
    #     "auth_permission",
    #     "django_admin_log",
    #     "django_migrations",
    #     "django_session",
    #     "users_groups",
    #     "user_user_permissions",
    # ])

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
