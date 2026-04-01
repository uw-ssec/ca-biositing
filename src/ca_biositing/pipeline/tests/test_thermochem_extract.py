"""Tests for Thermochem ETL extract functions."""

from unittest.mock import patch
import pandas as pd
import pytest
from ca_biositing.pipeline.etl.extract import thermochem_data

def test_extract_thermochem_imports():
    """Test that thermochem extractors can be imported."""
    assert thermochem_data.thermo_experiment is not None
    assert thermochem_data.thermo_data is not None
    assert thermochem_data.reaction_setup is not None
    assert thermochem_data.thermo_methods is not None
    assert thermochem_data.thermo_reactors is not None
    assert thermochem_data.thermo_parameters is not None
    assert thermochem_data.aim1_material_types is not None
    assert thermochem_data.aim1_preprocessing is not None

@patch("ca_biositing.pipeline.etl.extract.factory.get_run_logger")
@patch("ca_biositing.pipeline.utils.gsheet_to_pandas.gsheet_to_df")
def test_extract_thermo_data_success(mock_gsheet_to_df, mock_logger):
    """Test successful extraction of thermochem data."""
    # Mock the logger
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock the gsheet_to_df function
    test_data = pd.DataFrame({
        "experiment_id": ["EXP001", "EXP002"],
        "temperature": [500, 600]
    })
    mock_gsheet_to_df.return_value = test_data

    # Call the function directly
    result = thermochem_data.thermo_data.fn()

    # Verify results
    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    assert "experiment_id" in result.columns
    assert mock_gsheet_to_df.called
