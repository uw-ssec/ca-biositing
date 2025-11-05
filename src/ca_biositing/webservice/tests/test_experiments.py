"""Tests for experiments CRUD endpoints."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import status


@pytest.fixture
def mock_experiment():
    """Create a mock experiment object."""
    experiment = MagicMock()
    experiment.experiment_id = 1
    experiment.exper_uuid = "test-uuid"
    experiment.gsheet_exper_id = 1
    experiment.analysis_type_id = None
    experiment.analysis_abbrev_id = None
    experiment.exper_start_date = None
    experiment.exper_duration = None
    experiment.exper_duration_unit_id = None
    experiment.exper_location_id = None
    experiment.exper_description = "Test experiment"
    return experiment


def test_list_experiments(client, mock_experiment):
    """Test listing experiments."""
    with patch("ca_biositing.webservice.services.experiment_service.get_experiment_list") as mock_list:
        mock_list.return_value = ([mock_experiment], 1)
        
        response = client.get("/v1/experiments")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["experiment_id"] == 1


def test_get_experiment_by_id(client, mock_experiment):
    """Test getting a specific experiment by ID."""
    with patch("ca_biositing.webservice.services.experiment_service.get_experiment_by_id") as mock_get:
        mock_get.return_value = mock_experiment
        
        response = client.get("/v1/experiments/1")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["experiment_id"] == 1
        assert data["exper_description"] == "Test experiment"


def test_get_experiment_not_found(client):
    """Test getting a non-existent experiment."""
    with patch("ca_biositing.webservice.services.experiment_service.get_experiment_by_id") as mock_get:
        mock_get.return_value = None
        
        response = client.get("/v1/experiments/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_experiment(client, mock_experiment):
    """Test creating a new experiment."""
    with patch("ca_biositing.webservice.services.experiment_service.create_experiment") as mock_create:
        mock_create.return_value = mock_experiment
        
        experiment_data = {
            "exper_uuid": "test-uuid",
            "exper_description": "Test experiment"
        }
        
        response = client.post("/v1/experiments", json=experiment_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["experiment_id"] == 1


def test_update_experiment(client, mock_experiment):
    """Test updating an existing experiment."""
    with patch("ca_biositing.webservice.services.experiment_service.update_experiment") as mock_update:
        mock_update.return_value = mock_experiment
        
        update_data = {"exper_description": "Updated description"}
        
        response = client.put("/v1/experiments/1", json=update_data)
        assert response.status_code == status.HTTP_200_OK


def test_delete_experiment(client):
    """Test deleting an experiment."""
    with patch("ca_biositing.webservice.services.experiment_service.delete_experiment") as mock_delete:
        mock_delete.return_value = True
        
        response = client.delete("/v1/experiments/1")
        assert response.status_code == status.HTTP_200_OK
