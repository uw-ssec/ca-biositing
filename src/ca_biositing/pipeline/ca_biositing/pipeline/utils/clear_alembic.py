import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def clear_alembic_version():
    """Connects to the database and truncates the alembic_version table."""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        from ca_biositing.datamodels.config import settings
        database_url = settings.database_url

    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            connection.execute(text("TRUNCATE TABLE alembic_version;"))
            print("Successfully truncated alembic_version table.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    clear_alembic_version()
