"""Tests for ETL extract functions."""

from unittest.mock import patch
import pandas as pd


def test_extract_basic_sample_info_import():
    """Test that extract can be imported."""
    from ca_biositing.pipeline.etl.extract.basic_sample_info import extract
    assert extract is not None
    assert callable(extract.fn)  # Prefect task has .fn attribute


@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.get_run_logger")
@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.gsheet_to_df")
def test_extract_basic_sample_info_success(mock_gsheet_to_df, mock_logger):
    """Test successful extraction of basic sample info."""
    from ca_biositing.pipeline.etl.extract.basic_sample_info import extract

    # Mock the logger to avoid Prefect context issues
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock the gsheet_to_df function to return test data
    test_data = pd.DataFrame({
        "sample_name": ["Sample1", "Sample2"],
        "biomass_type": ["Type1", "Type2"]
    })
    mock_gsheet_to_df.return_value = test_data

    # Call the function directly (not as a Prefect task)
    result = extract.fn()

    # Verify results
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "sample_name" in result.columns


@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.get_run_logger")
@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.gsheet_to_df")
def test_extract_basic_sample_info_failure(mock_gsheet_to_df, mock_logger):
    """Test extraction failure handling."""
    from ca_biositing.pipeline.etl.extract.basic_sample_info import extract

    # Mock the logger to avoid Prefect context issues
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock the gsheet_to_df function to return None (failure)
    mock_gsheet_to_df.return_value = None

    # Call the function directly (not as a Prefect task)
    result = extract.fn()

    # Verify it returns None on failure
    assert result is None
