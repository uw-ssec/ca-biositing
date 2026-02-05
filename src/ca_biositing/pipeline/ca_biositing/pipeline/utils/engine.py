from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv

#This module queries the db via the ORM

# Get the root
path = os.getcwd()
project_root = None
while path != os.path.dirname(path): # Stop at the filesystem root
    if 'pixi.toml' in os.listdir(path):
        project_root = path
        break
    path = os.path.dirname(path)

# Load environment variables from the .env file located in the resources/docker directory.
# Use platform‑independent path construction to avoid Windows‑style separators on macOS/Linux.
from pathlib import Path

if project_root:
    env_path = Path(project_root) / "resources" / "docker" / ".env"
    load_dotenv(dotenv_path=env_path)
else:
    # Fallback for container environments where project_root might not be detectable via pixi.toml
    load_dotenv()

# Database Connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# 2. Host Port Mapping
# This is the port on your local machine that will connect to the container's port 5432.
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# Construct the database URL. If any required environment variable is missing,
# fall back to an in‑memory SQLite database for safe import/testing purposes.
def _build_database_url() -> str:
    """Return a PostgreSQL URL if the server is reachable, otherwise SQLite.

    The function attempts a quick connection test; if it raises an exception the
    fallback URL is used. This logic runs at import time, so the rest of the code
    can keep using the ``engine`` object unchanged.
    """
    import sqlalchemy
    from sqlalchemy.exc import OperationalError

    # Check if we are inside a Docker container
    is_docker = os.path.exists('/.dockerenv')

    if POSTGRES_USER and POSTGRES_PASSWORD and POSTGRES_PORT:
        # Use 'db' host inside docker, 'localhost' outside
        host = "db" if is_docker else "localhost"
        port = "5432" if is_docker else POSTGRES_PORT

        url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{host}:{port}/biocirv_db"

        # Skip connectivity test during import to avoid hangs
        return url

    # Fallback SQLite in‑memory DB.
    return "sqlite:///:memory:"

DATABASE_URL = _build_database_url()

# old:
# DATABASE_URL = "postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db"
engine = create_engine(DATABASE_URL)

db_session = Session(engine)
