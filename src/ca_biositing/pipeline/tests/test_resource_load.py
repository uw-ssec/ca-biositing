import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.load.resource import load_resource

@patch("ca_biositing.pipeline.etl.load.resource.get_engine")
@patch("ca_biositing.pipeline.etl.load.resource.Session")
def test_load_resource(mock_session_class, mock_get_engine):
    # 1. Setup Mock Data (matching the output of resource transform)
    transformed_data = pd.DataFrame({
        "name": ["almond hulls", "corn stover"],
        "resource_class_id": [1, 1],
        "resource_subclass_id": [10, 11],
        "primary_ag_product_id": [100, 101],
        "note": ["test note 1", "test note 2"],
        "etl_run_id": [1, 1],
        "lineage_group_id": [10, 10]
    })

    # 2. Setup Mocks
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session

    # Mock the connection context manager
    mock_conn = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn

    # Mock query behavior: first call returns None (insert), second call returns None (insert)
    mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]

    # 3. Run Load Task
    # Use .fn to bypass Prefect orchestration
    load_resource.fn(transformed_data)

    # 4. Assertions
    assert mock_session.add.call_count == 2
    assert mock_session.commit.called
