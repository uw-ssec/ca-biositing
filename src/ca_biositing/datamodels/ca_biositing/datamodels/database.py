from sqlmodel import SQLModel, create_engine, Session
from .config import settings

# Create engine using the database URL from settings
# echo=False by default to avoid verbose SQL logging
engine = create_engine(settings.database_url, echo=False)

def get_session():
    """
    Dependency that yields a database session.
    Useful for FastAPI dependencies.
    """
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """
    Create all tables defined in SQLModel metadata.
    """
    SQLModel.metadata.create_all(engine)

def get_engine():
    """
    Returns the database engine.
    """
    return engine
