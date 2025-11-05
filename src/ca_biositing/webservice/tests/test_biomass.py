"""Tests for biomass CRUD endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import status


@pytest.fixture
def mock_biomass():
    """Create a mock biomass object."""
    biomass = MagicMock()
    biomass.biomass_id = 1
    biomass.biomass_name = "Test Biomass"
    biomass.primary_product_id = None
    biomass.taxonomy_id = None
    biomass.biomass_type_id = None
    biomass.biomass_notes = "Test notes"
    return biomass


def test_list_biomass_empty(client):
    """Test listing biomass when database is empty."""
    with patch("ca_biositing.webservice.services.biomass_service.get_biomass_list") as mock_list:
        mock_list.return_value = ([], 0)
        
        response = client.get("/v1/biomass")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "items" in data
        assert "pagination" in data
        assert len(data["items"]) == 0
        assert data["pagination"]["total"] == 0


def test_list_biomass_with_data(client, mock_biomass):
    """Test listing biomass with data."""
    with patch("ca_biositing.webservice.services.biomass_service.get_biomass_list") as mock_list:
        mock_list.return_value = ([mock_biomass], 1)
        
        response = client.get("/v1/biomass")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["biomass_id"] == 1
        assert data["items"][0]["biomass_name"] == "Test Biomass"
        assert data["pagination"]["total"] == 1


def test_list_biomass_pagination(client, mock_biomass):
    """Test biomass list pagination."""
    with patch("ca_biositing.webservice.services.biomass_service.get_biomass_list") as mock_list:
        mock_list.return_value = ([mock_biomass], 10)
        
        response = client.get("/v1/biomass?skip=5&limit=10")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["pagination"]["skip"] == 5
        assert data["pagination"]["limit"] == 10
        assert data["pagination"]["total"] == 10


def test_get_biomass_by_id(client, mock_biomass):
    """Test getting a specific biomass by ID."""
    with patch("ca_biositing.webservice.services.biomass_service.get_biomass_by_id") as mock_get:
        mock_get.return_value = mock_biomass
        
        response = client.get("/v1/biomass/1")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["biomass_id"] == 1
        assert data["biomass_name"] == "Test Biomass"


def test_get_biomass_not_found(client):
    """Test getting a non-existent biomass."""
    with patch("ca_biositing.webservice.services.biomass_service.get_biomass_by_id") as mock_get:
        mock_get.return_value = None
        
        response = client.get("/v1/biomass/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data


def test_create_biomass(client, mock_biomass):
    """Test creating a new biomass entry."""
    with patch("ca_biositing.webservice.services.biomass_service.create_biomass") as mock_create:
        mock_create.return_value = mock_biomass
        
        biomass_data = {
            "biomass_name": "Test Biomass",
            "biomass_notes": "Test notes"
        }
        
        response = client.post("/v1/biomass", json=biomass_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["biomass_id"] == 1
        assert data["biomass_name"] == "Test Biomass"


def test_create_biomass_validation_error(client):
    """Test creating biomass with missing required fields."""
    response = client.post("/v1/biomass", json={})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_biomass(client, mock_biomass):
    """Test updating an existing biomass entry."""
    mock_biomass.biomass_name = "Updated Biomass"
    
    with patch("ca_biositing.webservice.services.biomass_service.update_biomass") as mock_update:
        mock_update.return_value = mock_biomass
        
        update_data = {"biomass_name": "Updated Biomass"}
        
        response = client.put("/v1/biomass/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["biomass_name"] == "Updated Biomass"


def test_update_biomass_not_found(client):
    """Test updating a non-existent biomass."""
    with patch("ca_biositing.webservice.services.biomass_service.update_biomass") as mock_update:
        mock_update.return_value = None
        
        update_data = {"biomass_name": "Updated Biomass"}
        
        response = client.put("/v1/biomass/999", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_biomass(client):
    """Test deleting a biomass entry."""
    with patch("ca_biositing.webservice.services.biomass_service.delete_biomass") as mock_delete:
        mock_delete.return_value = True
        
        response = client.delete("/v1/biomass/1")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data


def test_delete_biomass_not_found(client):
    """Test deleting a non-existent biomass."""
    with patch("ca_biositing.webservice.services.biomass_service.delete_biomass") as mock_delete:
        mock_delete.return_value = False
        
        response = client.delete("/v1/biomass/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
