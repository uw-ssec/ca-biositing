"""Pytest configuration and fixtures for pipeline tests."""

import pytest
from sqlmodel import create_engine, Session, SQLModel


@pytest.fixture(name="engine")
def engine_fixture():
    """Create an in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:")
    from ca_biositing.datamodels.schemas.generated.ca_biositing import LandiqRecord
    # LandiqRecord.metadata contains all tables because they are in the same Base/Metadata
    LandiqRecord.metadata.create_all(engine)
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session
