from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Create engine using the database URL from settings
# echo=False by default to avoid verbose SQL logging

def _get_engine():
    from .config import settings
    db_url = settings.database_url
    # Docker-aware URL adjustment
    if os.path.exists('/.dockerenv'):
        if "@db:" in db_url:
            db_url = db_url.replace("@db:", "@localhost:") # This is for host access, but inside docker we want 'db'
            # Actually, settings.py should handle this, but let's ensure it's correct for the environment
        if "localhost" in db_url and os.path.exists('/.dockerenv'):
             db_url = db_url.replace("localhost", "db")
    return create_engine(db_url, echo=False)

# Lazy initialization of engine and sessionmaker to avoid import-time hangs
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = _get_engine()
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

Base = declarative_base()

# For backward compatibility with existing code that expects 'engine'
def __getattr__(name):
    if name == "engine":
        return get_engine()
    raise AttributeError(f"module {__name__} has no attribute {name}")

def get_session():
    """
    Dependency that yields a database session.
    Useful for FastAPI dependencies.
    """
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()
