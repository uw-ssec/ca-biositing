"""Tests for the static_resource_info extract module."""

from unittest.mock import patch
import pandas as pd
import pytest
from ca_biositing.pipeline.etl.extract.static_resource_info import extract

def test_extract_static_resource_info_import():
    """Test that the extract function can be imported and is a Prefect task."""
    assert extract is not None
    assert hasattr(extract, "fn"), "extract should be a Prefect task"
    # In some Prefect versions, it might be a wrapper, but .fn should be the original function
    assert callable(extract.fn)

@patch("ca_biositing.pipeline.etl.extract.static_resource_info.get_run_logger")
@patch("ca_biositing.pipeline.etl.extract.static_resource_info.gsheet_to_df")
def test_extract_static_resource_info_success(mock_gsheet_to_df, mock_logger):
    """Test successful extraction of static resource information."""
    # Mock the logger to avoid Prefect context issues
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock the gsheet_to_df function to return test data
    test_data = pd.DataFrame({
        "resource_id": [1, 2],
        "resource_name": ["Resource A", "Resource B"],
        "category": ["Static", "Static"]
    })
    mock_gsheet_to_df.return_value = test_data

    # Call the underlying function directly via .fn
    result = extract.fn()

    # Verify results
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "resource_name" in result.columns

    # Verify mock call parameters
    # Note: We check against the default values in static_resource_info.py
    mock_gsheet_to_df.assert_called_once_with(
        "Static_resource_information",
        "static_resource_info",
        "credentials.json"
    )

@patch("ca_biositing.pipeline.etl.extract.static_resource_info.get_run_logger")
@patch("ca_biositing.pipeline.etl.extract.static_resource_info.gsheet_to_df")
def test_extract_static_resource_info_failure(mock_gsheet_to_df, mock_logger):
    """Test extraction failure handling when gsheet_to_df returns None."""
    # Mock the logger
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock the gsheet_to_df function to return None (simulating failure)
    mock_gsheet_to_df.return_value = None

    # Call the function
    result = extract.fn()

    # Verify it returns None on failure
    assert result is None
