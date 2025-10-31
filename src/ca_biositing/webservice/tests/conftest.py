"""Pytest configuration and shared fixtures."""

import pytest
from fastapi.testclient import TestClient

from ca_biositing.webservice.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application.

    Returns:
        TestClient: A FastAPI test client for making requests to the API.
    """
    return TestClient(app)
