import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.load.static_resource_info import (
    load_landiq_resource_mapping,
    load_resource_availability
)

@patch("ca_biositing.pipeline.etl.load.static_resource_info.get_local_engine")
@patch("ca_biositing.pipeline.etl.load.static_resource_info.Session")
def test_load_landiq_resource_mapping(mock_session_class, mock_get_engine):
    # 1. Setup Mock Data
    mapping_data = pd.DataFrame({
        "landiq_crop_name": [1, 2],
        "resource_id": [10, 20],
        "etl_run_id": [1, 1],
        "lineage_group_id": [100, 100]
    })

    # 2. Setup Mocks
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session

    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    # Mock query behavior: return None to trigger inserts
    # LandiqResourceMapping has two filters in the query
    mock_session.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    # 3. Run Load Task
    load_landiq_resource_mapping.fn(mapping_data)

    # 4. Assertions
    assert mock_session.add.call_count == 2
    assert mock_session.commit.called

@patch("ca_biositing.pipeline.etl.load.static_resource_info.get_local_engine")
@patch("ca_biositing.pipeline.etl.load.static_resource_info.Session")
def test_load_resource_availability(mock_session_class, mock_get_engine):
    # 1. Setup Mock Data
    availability_data = pd.DataFrame({
        "resource_id": [10, 20],
        "from_month": [1, 1],
        "to_month": [12, 12],
        "residue_factor_dry_tons_acre": [0.5, 1.2],
        "residue_factor_wet_tons_acre": [0.6, 1.5],
        "etl_run_id": [1, 1],
        "lineage_group_id": [100, 100]
    })

    # 2. Setup Mocks
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session

    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    # Mock query behavior: return None to trigger inserts
    # ResourceAvailability has two filters in the query if geoid is provided (none in our test data)
    # Actually, if geoid is None it still does query.filter(ResourceAvailability.geoid.is_(None))
    mock_session.query.return_value.filter.return_value.filter.return_value.first.return_value = None

    # 3. Run Load Task
    load_resource_availability.fn(availability_data)

    # 4. Assertions
    assert mock_session.add.call_count == 2
    assert mock_session.commit.called

def test_load_empty_data():
    with patch("ca_biositing.pipeline.etl.load.static_resource_info.get_run_logger"):
        # Should return early without error
        load_landiq_resource_mapping.fn(pd.DataFrame())
        load_resource_availability.fn(pd.DataFrame())
