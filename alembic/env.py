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
import importlib.util
from pathlib import Path

# --- Import generated models ---
# You can explicitly import your generated models here, or uncomment the
# code below to dynamically import them.
from schemas.generated.census_survey import *
from schemas.generated.geography import *

# # --- Dynamically import generated models ---
# # This code will dynamically import all Python files from the
# # schemas/generated directory. This is a convenience so that you don't have
# # to add a new import statement every time you generate a new model from a
# # LinkML schema.
# generated_path = Path(__file__).resolve().parents[1] / "schemas" / "generated"
# for file in os.listdir(generated_path):
#     if file.endswith(".py") and file != "__init__.py":
#         module_name = file[:-3]
#         spec = importlib.util.spec_from_file_location(module_name, generated_path / file)
#         module = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(module)

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
# Combine metadata from all models
# See: https://alembic.sqlalchemy.org/en/latest/autogenerate.html#affecting-the-autogenerate-process
for table in SQLModel.metadata.tables.values():
    table.tometadata(SQLModel.metadata)

target_metadata = SQLModel.metadata


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
