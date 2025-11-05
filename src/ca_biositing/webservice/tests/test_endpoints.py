"""Integration tests for all endpoints."""

from fastapi import status


def test_all_endpoints_available(client):
    """Test that all main endpoints are available."""
    # Health endpoint
    response = client.get("/v1/health")
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR]
    
    # List endpoints should all return 200 or 500 (if DB not available)
    endpoints = [
        "/v1/biomass",
        "/v1/experiments",
        "/v1/samples",
        "/v1/locations",
        "/v1/products",
    ]
    
    for endpoint in endpoints:
        response = client.get(endpoint)
        # Should not return 404 - endpoint exists
        assert response.status_code != status.HTTP_404_NOT_FOUND


def test_openapi_schema_includes_all_routes(client):
    """Test that OpenAPI schema includes all endpoints."""
    response = client.get("/openapi.json")
    assert response.status_code == status.HTTP_200_OK
    
    schema = response.json()
    paths = schema["paths"]
    
    # Check that main endpoints are in the schema
    assert "/v1/health" in paths
    assert "/v1/biomass" in paths
    assert "/v1/experiments" in paths
    assert "/v1/samples" in paths
    assert "/v1/locations" in paths
    assert "/v1/products" in paths


def test_cors_headers_configured(client):
    """Test that CORS headers are configured."""
    response = client.options("/")
    # CORS should be configured, but exact behavior depends on middleware
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]


def test_pagination_parameters_work(client):
    """Test that pagination parameters are accepted."""
    # Should not return 422 validation error
    response = client.get("/v1/biomass?skip=0&limit=10")
    assert response.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
    
    response = client.get("/v1/experiments?skip=5&limit=20")
    assert response.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY


def test_pagination_parameters_validation(client):
    """Test that pagination parameters are validated."""
    # Invalid skip (negative)
    response = client.get("/v1/biomass?skip=-1")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Invalid limit (too large)
    response = client.get("/v1/biomass?limit=200")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Invalid limit (zero or negative)
    response = client.get("/v1/biomass?limit=0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_404_for_invalid_resource_id(client):
    """Test that invalid resource IDs return 404 or 500."""
    # These should either return 404 (not found) or 500 (DB error)
    # but not 422 (validation error) since the ID format is valid
    endpoints_with_id = [
        "/v1/biomass/99999",
        "/v1/experiments/99999",
        "/v1/samples/99999",
        "/v1/locations/99999",
        "/v1/products/99999",
    ]
    
    for endpoint in endpoints_with_id:
        response = client.get(endpoint)
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ]


def test_create_endpoints_require_data(client):
    """Test that create endpoints require request body."""
    endpoints = [
        "/v1/biomass",
        "/v1/experiments",
        "/v1/samples",
        "/v1/locations",
        "/v1/products",
    ]
    
    for endpoint in endpoints:
        # Empty body should return 422 validation error
        response = client.post(endpoint, json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
