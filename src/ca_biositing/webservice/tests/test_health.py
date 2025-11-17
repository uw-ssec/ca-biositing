"""Tests for the health check endpoint."""

from unittest.mock import patch

from fastapi import status


def test_health_check_success(client):
    """Test health check endpoint with successful database connection."""
    response = client.get("/v1/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "database" in data
    assert data["version"] == "0.1.0"


def test_health_check_database_connection(client):
    """Test health check endpoint verifies database connection."""
    response = client.get("/v1/health")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    # Database status should be either "connected" or have error info
    assert "database" in data
    assert isinstance(data["database"], str)
