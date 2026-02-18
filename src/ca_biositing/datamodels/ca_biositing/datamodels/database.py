"""
Database connection and session management using SQLModel.

This module provides lazy-initialized database engine and session management
compatible with both standalone scripts and FastAPI dependencies.
"""

from sqlmodel import create_engine, Session


def _get_engine():
    """Create a SQLModel engine from settings."""
    from .config import settings
    return create_engine(settings.database_url, echo=False)


# Lazy initialization of engine to avoid import-time hangs
_engine = None


def get_engine():
    """Get or create the singleton database engine."""
    global _engine
    if _engine is None:
        _engine = _get_engine()
    return _engine


def get_session():
    """
    Dependency that yields a database session.
    Useful for FastAPI dependencies.

    Usage:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(get_engine()) as session:
        yield session


# For backward compatibility with existing code that expects 'engine'
def __getattr__(name):
    if name == "engine":
        return get_engine()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
