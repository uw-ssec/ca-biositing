import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from pathlib import Path
from dotenv import load_dotenv

# Path configuration
HERE = Path(__file__).parent.resolve()
PROJECT_ROOT = HERE.parent.resolve()

# Load environment variables from .env
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

# Configure Python path to include local source models
# This ensures Alembic uses the freshly generated models from the src directory
sys.path.insert(0, str(PROJECT_ROOT / "src/ca_biositing/datamodels"))

from ca_biositing.datamodels.schemas.generated import ca_biositing
from ca_biositing.datamodels.schemas.generated.ca_biositing import *
# Import Base for target metadata
from ca_biositing.datamodels.database import Base

# Alembic Config object
config = context.config

# Configure database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise RuntimeError("DATABASE_URL not found in .env file. Alembic cannot run migrations.")

# Setup Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate support
target_metadata = Base.metadata


def include_object(obj, name, type_, reflected, compare_to):
    """
    Filter objects for autogenerate to prevent unwanted schema changes.
    """
    # Exclude PostGIS system tables
    if type_ == "table" and name in [
        "spatial_ref_sys",
        "geometry_columns",
        "geography_columns",
        "raster_columns",
        "raster_overviews",
    ]:
        return False

    # Exclude tables from non-public schemas (e.g., tiger, topology)
    if type_ == "table" and hasattr(obj, "schema") and obj.schema is not None:
        return False

    # Ignore unique constraints on primary key columns to avoid redundant diffs
    if type_ == "unique_constraint" and obj is not None:
        cols = [c.name for c in obj.columns]
        table = obj.table
        pk_cols = [c.name for c in table.primary_key.columns]
        if cols == pk_cols:
            return False

    return True

# Manually merge metadata from generated modules
# for table in census_metadata.tables.values():
#     table.tometadata(target_metadata)
#
# for table in geography_metadata.tables.values():
#     table.tometadata(target_metadata)


def render_item(type_, obj, autogen_context):
    """
    Add custom imports to the migration template.
    """
    if type_ == "type" and hasattr(obj, "__module__"):
        if obj.__module__.startswith("sqlmodel"):
            autogen_context.imports.add("import sqlmodel")
    return False


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    Configures the context with a URL and without an active connection.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_item=render_item,
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    Creates an Engine and associates a connection with the context.
    """
    config_section = config.get_section(config.config_ini_section, {})

    # Restrict search_path to 'public' to avoid reflecting PostGIS system tables
    connect_args = {"options": "-c search_path=public"}

    connectable = engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_item=render_item,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
