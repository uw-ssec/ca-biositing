"""Tests for the main FastAPI application."""

from fastapi import status


def test_read_root(client):
    """Test the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "CA Biositing API"


def test_read_hello(client):
    """Test the hello endpoint returns expected response."""
    response = client.get("/hello")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert data["message"] == "Hello, world"


def test_openapi_docs_available(client):
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == status.HTTP_200_OK


def test_openapi_json_available(client):
    """Test that OpenAPI JSON schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "CA Biositing API"


def test_imports_inline():
    """Test inline imports work."""
    # Should be able to import the app directly
    from ca_biositing.webservice.main import app

    assert app is not None
    assert hasattr(app, "title")
    assert app.title == "CA Biositing API"


def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == status.HTTP_404_NOT_FOUND
