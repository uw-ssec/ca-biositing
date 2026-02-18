from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

# This module queries the db via the ORM

# Get the root
path = os.getcwd()
project_root = None
while path != os.path.dirname(path):  # Stop at the filesystem root
    if 'pixi.toml' in os.listdir(path):
        project_root = path
        break
    path = os.path.dirname(path)

# Load environment variables from the .env file located in the resources/docker directory.
if project_root:
    env_path = Path(project_root) / "resources" / "docker" / ".env"
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback for container environments where project_root might not be detectable via pixi.toml
    load_dotenv()

# Database Connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")


def _build_database_url() -> str:
    """Return a PostgreSQL URL if the server is reachable, otherwise SQLite."""
    # Check if we are inside a Docker container
    is_docker = os.path.exists('/.dockerenv')

    if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_PORT:
        # Use 'db' host inside docker, 'localhost' outside
        host = "db" if is_docker else "localhost"
        port = "5432" if is_docker else POSTGRES_PORT

        url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}:{port}/biocirv_db"
        return url

    # Fallback SQLite in‑memory DB.
    return "sqlite:///:memory:"


DATABASE_URL = _build_database_url()

# Global engine instance with pooling options
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=0,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10}
)

db_session = Session(engine)


def get_local_engine():
    """
    Returns the shared engine instance.
    Maintained for backward compatibility with modules that previously defined it locally.
    """
    return engine
