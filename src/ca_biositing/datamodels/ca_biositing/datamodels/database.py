"""Database connection and session management for CA Biositing data models."""

from __future__ import annotations

from typing import Generator

from sqlmodel import Session, create_engine

from ca_biositing.datamodels.config import config

# Create database engine
engine = create_engine(
    config.database_url,
    echo=config.echo_sql,
    pool_size=config.pool_size,
    max_overflow=config.max_overflow,
)


def get_session() -> Generator[Session, None, None]:
    """Get a database session.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
