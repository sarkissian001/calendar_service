# import asyncio
# import os
# import sys
# from logging.config import fileConfig
#
# from sqlalchemy import pool
# from sqlalchemy.ext.asyncio import create_async_engine
# from alembic import context
# from dotenv import load_dotenv
#
# # Load environment variables from a .env file if it exists
# load_dotenv()
#
# # Dynamically add the root directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#
# from app.models.event_models import Base  # Now this should work
#
# # Interpret the config file for Python logging.
# config = context.config
# fileConfig(config.config_file_name)
#
# # Set up the target metadata (from your models)
# target_metadata = Base.metadata
#
# # Set the SQLAlchemy URL dynamically using environment variables
# config.set_main_option(
#     "sqlalchemy.url",
#     f"postgresql+asyncpg://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
# )
#
# def run_migrations_offline():
#     """Run migrations in 'offline' mode."""
#     url = config.get_main_option("sqlalchemy.url")
#     context.configure(
#         url=url,
#         target_metadata=target_metadata,
#         literal_binds=True,
#         dialect_opts={"paramstyle": "named"},
#     )
#
#     with context.begin_transaction():
#         context.run_migrations()
#
#
# async def run_migrations_online():
#     """Run migrations in 'online' mode."""
#     try:
#         connectable = create_async_engine(
#             config.get_main_option("sqlalchemy.url"),
#             poolclass=pool.NullPool,
#         )
#     except Exception as e:
#         print("Failed to create async engine:", e)
#         sys.exit(1)
#
#     async with connectable.connect() as connection:
#         await connection.run_sync(do_run_migrations)
#
#     await connectable.dispose()
#
#
# def do_run_migrations(connection):
#     context.configure(
#         connection=connection,
#         target_metadata=target_metadata,
#         compare_type=True,
#     )
#
#     with context.begin_transaction():
#         context.run_migrations()
#
#
# if context.is_offline_mode():
#     run_migrations_offline()
# else:
#     asyncio.run(run_migrations_online())

import os
import sys
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.event_models import Base  # Import your Base from your models

# Interpret the config file for Python logging.
config = context.config
fileConfig(config.config_file_name)

# Set up the target metadata from your models
target_metadata = Base.metadata

# Configure SQLAlchemy URL using environment variables
config.set_main_option(
    "sqlalchemy.url",
    f"postgresql+asyncpg://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}"
)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    # import pdb; pdb.set_trace()
    context.configure(
        url=url,
        transactional_ddl=False,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.execute("-- running migrations offline '%s'")
        context.run_migrations()

async def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

if os.getenv("RUN_ALCHEMIC_OFFLINE", "False").lower() == "true":
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
