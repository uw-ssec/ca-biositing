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
from ca_biositing.datamodels.biomass import *
from ca_biositing.datamodels.data_and_references import *
from ca_biositing.datamodels.experiments_analysis import *
from ca_biositing.datamodels.external_datasets import *
from ca_biositing.datamodels.geographic_locations import *
from ca_biositing.datamodels.metadata_samples import *
from ca_biositing.datamodels.organizations import *
from ca_biositing.datamodels.people_contacts import *
from ca_biositing.datamodels.sample_preprocessing import *
from ca_biositing.datamodels.specific_aalysis_results import *
from ca_biositing.datamodels.user import *
from sqlmodel import SQLModel

# --- Alembic Config object, provides access to alembic.ini values ---
config = context.config

# Override sqlalchemy.url in alembic.ini with value from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise RuntimeError("DATABASE_URL not found in .env file. Alembic cannot run migrations.")

# --- Configure logging (from alembic.ini logging section) ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Metadata from your models for autogenerate ---
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
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
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
