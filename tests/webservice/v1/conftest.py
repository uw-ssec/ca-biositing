"""Pytest fixtures for v1 API endpoint tests.

This module provides shared test fixtures including database setup,
test data, and test client configuration.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ca_biositing.datamodels.database import get_session
from sqlmodel import SQLModel
from ca_biositing.datamodels.models import (
    DimensionType,
    Observation,
    Parameter,
    Resource,
    ResourceUsdaCommodityMap,
    Unit,
    UsdaCensusRecord,
    UsdaCommodity,
)
from ca_biositing.webservice.main import app


@pytest.fixture(name="engine", scope="function")
def engine_fixture():
    """Create in-memory SQLite engine for testing.

    Returns:
        SQLAlchemy engine configured for testing
    """
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},  # Allow multi-threading for tests
        poolclass=None,  # Disable connection pooling for in-memory DB
    )

    # Manually create only the tables we need (avoiding Polygon with md5())
    with engine.begin() as connection:
        Unit.__table__.create(connection, checkfirst=True)
        DimensionType.__table__.create(connection, checkfirst=True)
        Parameter.__table__.create(connection, checkfirst=True)
        UsdaCommodity.__table__.create(connection, checkfirst=True)
        Resource.__table__.create(connection, checkfirst=True)
        ResourceUsdaCommodityMap.__table__.create(connection, checkfirst=True)
        UsdaCensusRecord.__table__.create(connection, checkfirst=True)
        Observation.__table__.create(connection, checkfirst=True)

    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create test database session.

    Args:
        engine: SQLAlchemy engine fixture

    Yields:
        Database session for testing
    """
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session):
    """Create test client with overridden database session.

    Args:
        session: Database session fixture

    Yields:
        FastAPI test client
    """
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_census_data")
def test_census_data_fixture(session: Session):
    """Create test census data in database.

    This fixture creates:
    - CORN and SOYBEANS commodities
    - corn_grain and soybean_meal resources
    - Census records for geoid 06001
    - Observations with parameters, units, and dimensions

    Args:
        session: Database session fixture

    Returns:
        Dictionary with test data IDs
    """
    # Create units
    unit_acres = Unit(id=1, name="acres")
    unit_bushels = Unit(id=2, name="bushels")
    unit_tons = Unit(id=3, name="tons")
    session.add_all([unit_acres, unit_bushels, unit_tons])

    # Create dimension types
    dim_type_area = DimensionType(id=1, name="area")
    session.add(dim_type_area)

    # Create parameters
    param_acres = Parameter(id=1, name="acres", standard_unit_id=1)
    param_production = Parameter(id=2, name="production", standard_unit_id=2)
    param_yield = Parameter(id=3, name="yield_per_acre", standard_unit_id=2)
    session.add_all([param_acres, param_production, param_yield])

    # Create commodities
    commodity_corn = UsdaCommodity(id=1, name="CORN", usda_code="00090")
    commodity_soybeans = UsdaCommodity(id=2, name="SOYBEANS", usda_code="00081")
    session.add_all([commodity_corn, commodity_soybeans])

    # Create resources
    resource_corn_grain = Resource(id=1, name="corn_grain", primary_ag_product_id=1)
    resource_soybean_meal = Resource(id=2, name="soybean_meal", primary_ag_product_id=2)
    session.add_all([resource_corn_grain, resource_soybean_meal])

    # Create resource-commodity mappings
    mapping_corn = ResourceUsdaCommodityMap(
        id=1,
        resource_id=1,
        usda_commodity_id=1,
        match_tier="exact"
    )
    mapping_soybean = ResourceUsdaCommodityMap(
        id=2,
        resource_id=2,
        usda_commodity_id=2,
        match_tier="exact"
    )
    session.add_all([mapping_corn, mapping_soybean])

    # Create census records
    census_corn = UsdaCensusRecord(
        id=1,
        dataset_id=1,
        geoid="06001",
        commodity_code=1,
        year=2022
    )
    census_soybeans = UsdaCensusRecord(
        id=2,
        dataset_id=1,
        geoid="06001",
        commodity_code=2,
        year=2022
    )
    session.add_all([census_corn, census_soybeans])

    # Create observations for CORN
    # IMPORTANT: record_id must be unique AND should reference the census record
    # We use a format like "census_{census_record_id}_{param_id}" for uniqueness
    obs_corn_acres = Observation(
        id=1,
        record_id="census_1_acres",
        dataset_id=1,
        record_type="census",
        parameter_id=1,
        value=25000.0,
        unit_id=1,
    )
    obs_corn_production = Observation(
        id=2,
        record_id="census_1_production",
        dataset_id=1,
        record_type="census",
        parameter_id=2,
        value=3750000.0,
        unit_id=2,
    )
    obs_corn_yield = Observation(
        id=3,
        record_id="census_1_yield",
        dataset_id=1,
        record_type="census",
        parameter_id=3,
        value=150.0,
        unit_id=2,
        dimension_type_id=1,
        dimension_value=1.0,
        dimension_unit_id=1,
    )

    # Create observations for SOYBEANS
    obs_soybeans_acres = Observation(
        id=4,
        record_id="census_2_acres",
        dataset_id=1,
        record_type="census",
        parameter_id=1,
        value=15000.0,
        unit_id=1,
    )

    session.add_all([
        obs_corn_acres,
        obs_corn_production,
        obs_corn_yield,
        obs_soybeans_acres,
    ])
    session.commit()

    return {
        "commodity_corn_id": 1,
        "commodity_soybeans_id": 2,
        "resource_corn_id": 1,
        "resource_soybean_id": 2,
        "census_corn_id": 1,
        "census_soybeans_id": 2,
    }
