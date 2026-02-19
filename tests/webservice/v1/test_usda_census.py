"""Tests for USDA Census data API endpoints.

This module tests all four census endpoint patterns:
- Get single parameter by crop
- Get single parameter by resource
- List all parameters by crop
- List all parameters by resource
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestGetCensusByCrop:
    """Test cases for getting census data by USDA crop name."""

    def test_get_single_parameter_success(self, client: TestClient, test_census_data):
        """Test successful retrieval of single parameter by crop."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters/acres"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["usda_crop"] == "CORN"
        assert data["resource"] is None
        assert data["geoid"] == "06001"
        assert data["parameter"] == "acres"
        assert data["value"] == 25000.0
        assert data["unit"] == "acres"

    def test_get_parameter_with_dimension(self, client: TestClient, test_census_data):
        """Test retrieval of parameter with dimension data."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters/yield_per_acre"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["parameter"] == "yield_per_acre"
        assert data["value"] == 150.0
        assert data["dimension"] == "area"
        assert data["dimension_value"] == 1.0
        assert data["dimension_unit"] == "acres"

    def test_crop_not_found(self, client: TestClient, test_census_data):
        """Test 404 when crop doesn't exist."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/FAKE_CROP/geoid/06001/parameters/acres"
        )

        assert response.status_code == 404
        assert "FAKE_CROP" in response.json()["detail"]
        assert "not found" in response.json()["detail"].lower()

    def test_parameter_not_found_for_crop(self, client: TestClient, test_census_data):
        """Test 404 when parameter doesn't exist for crop/geoid."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters/nonexistent_param"
        )

        assert response.status_code == 404
        assert "nonexistent_param" in response.json()["detail"]
        assert "not found" in response.json()["detail"].lower()

    def test_geoid_not_found(self, client: TestClient, test_census_data):
        """Test 404 when geoid has no data for crop."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/99999/parameters/acres"
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestGetCensusByResource:
    """Test cases for getting census data by resource name."""

    def test_get_single_parameter_success(self, client: TestClient, test_census_data):
        """Test successful retrieval of single parameter by resource."""
        response = client.get(
            "/v1/feedstocks/usda/census/resources/corn_grain/geoid/06001/parameters/acres"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["usda_crop"] is None
        assert data["resource"] == "corn_grain"
        assert data["geoid"] == "06001"
        assert data["parameter"] == "acres"
        assert data["value"] == 25000.0
        assert data["unit"] == "acres"

    def test_resource_not_found(self, client: TestClient, test_census_data):
        """Test 404 when resource doesn't exist."""
        response = client.get(
            "/v1/feedstocks/usda/census/resources/fake_resource/geoid/06001/parameters/acres"
        )

        assert response.status_code == 404
        assert "fake_resource" in response.json()["detail"]
        assert "not found" in response.json()["detail"].lower()

    def test_parameter_not_found_for_resource(self, client: TestClient, test_census_data):
        """Test 404 when parameter doesn't exist for resource/geoid."""
        response = client.get(
            "/v1/feedstocks/usda/census/resources/corn_grain/geoid/06001/parameters/fake_param"
        )

        assert response.status_code == 404
        assert "fake_param" in response.json()["detail"]
        assert "not found" in response.json()["detail"].lower()


class TestListCensusByCrop:
    """Test cases for listing all census parameters by crop."""

    def test_list_all_parameters_success(self, client: TestClient, test_census_data):
        """Test successful listing of all parameters for crop."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["usda_crop"] == "CORN"
        assert data["resource"] is None
        assert data["geoid"] == "06001"
        assert "data" in data
        assert len(data["data"]) == 3  # acres, production, yield_per_acre

        # Check that all expected parameters are present
        params = [item["parameter"] for item in data["data"]]
        assert "acres" in params
        assert "production" in params
        assert "yield_per_acre" in params

    def test_list_parameters_structure(self, client: TestClient, test_census_data):
        """Test that list response has correct structure."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters"
        )

        assert response.status_code == 200
        data = response.json()

        # Verify each data item has required fields
        for item in data["data"]:
            assert "parameter" in item
            assert "value" in item
            assert "unit" in item
            assert isinstance(item["value"], (int, float))
            assert isinstance(item["unit"], str)

    def test_list_crop_not_found(self, client: TestClient, test_census_data):
        """Test 404 when listing parameters for nonexistent crop."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/FAKE_CROP/geoid/06001/parameters"
        )

        assert response.status_code == 404
        assert "FAKE_CROP" in response.json()["detail"]

    def test_list_no_data_for_geoid(self, client: TestClient, test_census_data):
        """Test 404 when no data exists for crop/geoid combination."""
        response = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/99999/parameters"
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestListCensusByResource:
    """Test cases for listing all census parameters by resource."""

    def test_list_all_parameters_success(self, client: TestClient, test_census_data):
        """Test successful listing of all parameters for resource."""
        response = client.get(
            "/v1/feedstocks/usda/census/resources/corn_grain/geoid/06001/parameters"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["usda_crop"] is None
        assert data["resource"] == "corn_grain"
        assert data["geoid"] == "06001"
        assert "data" in data
        assert len(data["data"]) == 3

    def test_list_resource_not_found(self, client: TestClient, test_census_data):
        """Test 404 when listing parameters for nonexistent resource."""
        response = client.get(
            "/v1/feedstocks/usda/census/resources/fake_resource/geoid/06001/parameters"
        )

        assert response.status_code == 404
        assert "fake_resource" in response.json()["detail"]


class TestParameterValidation:
    """Test cases for URL path validation logic.

    Note: With RESTful paths, FastAPI handles most validation automatically.
    Invalid URLs return 404 instead of 422.
    """

    def test_invalid_url_pattern(self, client: TestClient, test_census_data):
        """Test 404 when using invalid URL pattern."""
        # Try to access non-existent endpoint
        response = client.get(
            "/v1/feedstocks/usda/census/invalid/path"
        )

        assert response.status_code == 404


class TestMultipleCrops:
    """Test cases with multiple crops to ensure correct filtering."""

    def test_get_different_crops(self, client: TestClient, test_census_data):
        """Test that different crops return different data."""
        # Get CORN data
        response_corn = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters/acres"
        )

        # Get SOYBEANS data
        response_soybeans = client.get(
            "/v1/feedstocks/usda/census/crops/SOYBEANS/geoid/06001/parameters/acres"
        )

        assert response_corn.status_code == 200
        assert response_soybeans.status_code == 200

        corn_data = response_corn.json()
        soybean_data = response_soybeans.json()

        # Values should be different
        assert corn_data["value"] == 25000.0
        assert soybean_data["value"] == 15000.0
        assert corn_data["usda_crop"] == "CORN"
        assert soybean_data["usda_crop"] == "SOYBEANS"

    def test_list_different_crops_different_counts(self, client: TestClient, test_census_data):
        """Test that different crops have different parameter counts."""
        # CORN has 3 parameters
        response_corn = client.get(
            "/v1/feedstocks/usda/census/crops/CORN/geoid/06001/parameters"
        )

        # SOYBEANS has 1 parameter
        response_soybeans = client.get(
            "/v1/feedstocks/usda/census/crops/SOYBEANS/geoid/06001/parameters"
        )

        assert response_corn.status_code == 200
        assert response_soybeans.status_code == 200

        assert len(response_corn.json()["data"]) == 3
        assert len(response_soybeans.json()["data"]) == 1
