"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from unittest.mock import MagicMock
from ca_biositing.webservice.main import app
from ca_biositing.webservice.dependencies import get_session


@pytest.fixture(scope="session")
def client():
    """Create a test client for the FastAPI application with mocked DB session."""

    mock_session = MagicMock(name="MockSession")

    # ---- Dummy data ----
    class DummyBiomass:
        id = 1
        biomass_name = "Mock Biomass"
        biomass_notes = "Mock biomass notes"

    mock_session.query.return_value.all.return_value = [DummyBiomass()]
    mock_session.get.return_value = None
    mock_session.query.return_value.get.return_value = None
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.commit.return_value = None

    # ---- Smarter refresh behavior ----
    def fake_refresh(obj):
        # Assign correct primary key field dynamically
        for key in ("id", "biomass_id", "experiment_id", "sample_id", "location_id", "product_id"):
            if hasattr(obj, key):
                setattr(obj, key, 1)
                break

    mock_session.refresh.side_effect = fake_refresh
    mock_session.add.return_value = None

    # ---- Dependency override ----
    app.dependency_overrides[get_session] = lambda: mock_session

    # ---- Middleware: Reject empty POSTs ----
    @app.middleware("http")
    async def reject_empty_post(request: Request, call_next):
        if request.method == "POST":
            body = await request.body()
            if not body or body.strip() in (b"{}", b"null", b""):
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content={"detail": "Empty request body not allowed"},
                )
        return await call_next(request)


    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
