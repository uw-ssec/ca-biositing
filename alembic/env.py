import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Add project root to python path ---
# This allows alembic to find the 'src' package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# --- Load environment variables from .env ---
from dotenv import load_dotenv
load_dotenv()  # Looks for .env in the project root by default

# --- Import your models so Alembic knows about them ---
from src.pipeline.etl.models.biomass import *
from src.pipeline.etl.models.data_and_references import *
from src.pipeline.etl.models.experiments_analysis import *
from src.pipeline.etl.models.external_datasets import *
from src.pipeline.etl.models.geographic_locations import *
from src.pipeline.etl.models.metadata_samples import *
from src.pipeline.etl.models.organizations import *
from src.pipeline.etl.models.people_contacts import *
from src.pipeline.etl.models.sample_preprocessing import *
from src.pipeline.etl.models.specific_aalysis_results import *
from src.pipeline.etl.models.user import *
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
