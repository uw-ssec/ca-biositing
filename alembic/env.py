import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path
from dotenv import load_dotenv

HERE = Path(__file__).parent.resolve()
PROJECT_ROOT = HERE.parent.resolve()

# --- Load environment variables from .env ---
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")  # Looks for .env in the project root by default

# --- Import your models so Alembic knows about them ---
from ca_biositing.datamodels.schemas.generated import ca_biositing
from ca_biositing.datamodels.schemas.generated.ca_biositing import *
# from ca_biositing.datamodels.database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url in alembic.ini with value from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise RuntimeError("DATABASE_URL not found in .env file. Alembic cannot run migrations.")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# Manually merge metadata from generated modules
# for table in census_metadata.tables.values():
#     table.tometadata(target_metadata)
#
# for table in geography_metadata.tables.values():
#     table.tometadata(target_metadata)


def render_item(type_, obj, autogen_context):
    """Add custom imports to the migration template."""
    if type_ == "type" and hasattr(obj, "__module__"):
        if obj.__module__.startswith("sqlmodel"):
            autogen_context.imports.add("import sqlmodel")
    return False


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
