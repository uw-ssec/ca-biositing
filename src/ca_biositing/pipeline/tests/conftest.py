"""Pytest configuration and fixtures for pipeline tests."""

import hashlib
import pytest
from sqlalchemy import event
from sqlmodel import create_engine, Session, SQLModel


@pytest.fixture(name="engine")
def engine_fixture():
    """Create an in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:")

    # Register a mock md5 function for SQLite to support unique indexes on geometries
    @event.listens_for(engine, "connect")
    def receive_connect(dbapi_connection, connection_record):
        def sqlite_md5(value):
            if value is None:
                return None
            return hashlib.md5(str(value).encode()).hexdigest()

        dbapi_connection.create_function("md5", 1, sqlite_md5, deterministic=True)

    from ca_biositing.datamodels.models import LandiqRecord
    # LandiqRecord.metadata contains all tables because they are in the same Base/Metadata
    LandiqRecord.metadata.create_all(engine)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session
