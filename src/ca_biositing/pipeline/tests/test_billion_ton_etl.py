"""Tests for Billion Ton ETL modules."""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from ca_biositing.pipeline.etl.extract.billion_ton import extract
from ca_biositing.pipeline.etl.transform.billion_ton import transform
from ca_biositing.pipeline.etl.load.billion_ton import load

@pytest.fixture
def sample_billion_ton_df():
    return pd.DataFrame({
        "class": ["agriculture land", "agriculture land"],
        "subclass": ["Agricultural residues", "Agricultural residues"],
        "resource": ["Corn stover", "Barley straw"],
        "fips": [6001, 6037],
        "county": ["Alameda County", "Los Angeles County"],
        "state_name": ["California", "California"],
        "usdaregion": ["Pacific", "Pacific"],
        "County Square Miles": [739.02, 4058.01],
        "model_name": ["POLYSYS", "POLYSYS"],
        "scenario_name": ["mature-market high", "emerging"],
        "price_offered": [70, 70],
        "production": [100.0, 200.0],
        "production_unit": ["dt", "dt"],
        "btu_ton": [15722000, 14892000],
        "production_energy_content": [1572200, 2978400],
        "energy_content_unit": ["BTU", "BTU"],
        "production_density_dtpersqmi": [0.13, 0.05],
        "landsource": ["Crop", "Crop"]
    })

# --- Extract Tests ---

@patch("ca_biositing.pipeline.etl.extract.billion_ton.get_run_logger")
@patch("ca_biositing.pipeline.utils.gdrive_to_pandas.gdrive_to_df")
@patch("tempfile.TemporaryDirectory")
def test_extract_success(mock_temp_dir, mock_gdrive_to_df, mock_logger):
    # Setup mock temp dir context manager
    mock_temp_dir_instance = MagicMock()
    mock_temp_dir_instance.__enter__.return_value = "/tmp/fake_dir"
    mock_temp_dir.return_value = mock_temp_dir_instance

    test_df = pd.DataFrame({"test": [1, 2]})
    mock_gdrive_to_df.return_value = test_df

    result = extract.fn(file_id="fake_id", file_name="fake.csv")

    assert result is not None
    assert len(result) == 2
    mock_gdrive_to_df.assert_called_once()
    args, kwargs = mock_gdrive_to_df.call_args
    assert kwargs["file_id"] == "fake_id"
    assert kwargs["file_name"] == "fake.csv"
    assert kwargs["dataset_folder"] == "/tmp/fake_dir"

@patch("ca_biositing.pipeline.etl.extract.billion_ton.get_run_logger")
@patch("ca_biositing.pipeline.utils.gdrive_to_pandas.gdrive_to_df")
@patch("tempfile.TemporaryDirectory")
def test_extract_failure(mock_temp_dir, mock_gdrive_to_df, mock_logger):
    # Setup mock temp dir
    mock_temp_dir_instance = MagicMock()
    mock_temp_dir_instance.__enter__.return_value = "/tmp/fake_dir"
    mock_temp_dir.return_value = mock_temp_dir_instance

    mock_gdrive_to_df.return_value = None

    result = extract.fn(file_id="invalid_id")
    assert result is None

# --- Transform Tests ---

@patch("ca_biositing.pipeline.etl.transform.billion_ton.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.billion_ton.normalize_dataframes")
def test_transform_success(mock_normalize, mock_logger, sample_billion_ton_df):
    # Setup mock normalize to return the same dataframe but with name_id columns
    def side_effect(df, normalize_columns):
        df_copy = df.copy()
        # In billion_ton.py:
        # dataset_name -> dataset_name_id -> dataset_id
        # production_unit_name -> production_unit_name_id -> production_unit_id
        # energy_content_unit_name -> energy_content_unit_name_id -> energy_content_unit_id
        # subclass -> subclass_id
        # resource -> resource_id
        for col in normalize_columns.keys():
            df_copy[f"{col}_id"] = 1
        return df_copy

    mock_normalize.side_effect = side_effect

    data_sources = {"billion_ton": sample_billion_ton_df}
    result = transform.fn(data_sources, etl_run_id=1, lineage_group_id=1)

    assert result is not None
    assert not result.empty
    assert "geoid" in result.columns
    # California FIPS 6001 -> GEOID 06001
    assert result["geoid"].iloc[0] == "06001"
    # Check county name cleaning (should be lowercase and without " county")
    assert result["county"].iloc[0] == "alameda"
    assert "dataset_id" in result.columns
    assert "subclass_id" in result.columns
    # Note: normalize_columns in billion_ton.py uses 'production_unit_name'
    # which becomes 'production_unit_name_id' and is then renamed to 'production_unit_id'
    assert "production_unit_id" in result.columns

@patch("ca_biositing.pipeline.etl.transform.billion_ton.get_run_logger")
def test_transform_filter_california(mock_logger, sample_billion_ton_df):
    """
    Verify that only California records are retained and coordinates/counties are normalized.
    This test uses the full sample_billion_ton_df fixture to ensure rename/coercion/normalization
    logic in transform.fn is exercised, while mocking normalize_dataframes to avoid DB connection.
    """
    # Create a mixed dataframe with CA and non-CA records
    df_mixed = sample_billion_ton_df.copy()
    df_mixed = pd.concat([
        df_mixed,
        pd.DataFrame({
            "class": ["agriculture land"],
            "subclass": ["Agricultural residues"],
            "resource": ["Corn stover"],
            "fips": [48001], # Texas
            "county": ["Harris County"],
            "state_name": ["Texas"],
            "usdaregion": ["Southern Plains"],
            "County Square Miles": [1777.0],
            "model_name": ["POLYSYS"],
            "scenario_name": ["mature-market high"],
            "price_offered": [70],
            "production": [500.0],
            "production_unit": ["dt"],
            "btu_ton": [15722000],
            "production_energy_content": [7861000],
            "energy_content_unit": ["BTU"],
            "production_density_dtpersqmi": [0.28],
            "landsource": ["Crop"]
        })
    ], ignore_index=True)

    data_sources = {"billion_ton": df_mixed}

    # We mock normalize_dataframes to avoid DB connection
    with patch("ca_biositing.pipeline.etl.transform.billion_ton.normalize_dataframes", side_effect=lambda df, cols: df):
        result = transform.fn(data_sources)
        # Should only have California records (2 from fixture)
        assert len(result) == 2
        assert all(result["state_name"] == "california")
        assert result["geoid"].iloc[0] == "06001"
        assert result["county"].iloc[0] == "alameda"

# --- Load Tests ---

@patch("ca_biositing.pipeline.etl.load.billion_ton.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.billion_ton.get_local_engine")
@patch("ca_biositing.pipeline.etl.load.billion_ton.Session")
def test_load_success(mock_session, mock_engine, mock_logger):
    df = pd.DataFrame({
        "geoid": ["06001"],
        "county": ["alameda"],
        "state_name": ["california"],
        "production": [100],
        "dataset_id": [1],
        "subclass_id": [2],
        "resource_id": [3],
        "production_unit_id": [4],
        "energy_content_unit_id": [5],
        "scenario_name": ["test-scenario"],
        "price_offered": [70.0],
        "production_density_dtpersqmi": [0.1],
        "etl_run_id": [1],
        "lineage_group_id": [1]
    })

    # Mocking the session and its execution
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    load.fn(df)

    # Check if session was created and committed
    assert mock_session.called
    session_instance = mock_session.return_value.__enter__.return_value
    # Place insert + Record insert
    assert session_instance.execute.call_count >= 2
    assert session_instance.commit.called

    # Inspect call arguments to verify payloads
    calls = session_instance.execute.call_args_list

    # Find the Place upsert (should contain geoid)
    place_call = next(
        (c for c in calls if hasattr(c.args[0], 'table') and c.args[0].table.name == 'place'),
        None
    )
    if place_call:
        # Extract parameters from the compiled statement
        stmt = place_call.args[0]
        params = stmt.compile().params
        # Multi-row insert parameters are often in list/dict form
        # We check if the expected values exist in any of the inserted rows
        found_geoid = False
        # params can be a list of dicts for multi-row values([...])
        # Or a single dict with numbered keys depending on the dialect
        # Here we just look for string containment in the string representation of params
        assert "06001" in str(params)
        assert "alameda" in str(params)

    # Find the BillionTon2023Record insert
    record_call = next(
        (c for c in calls if hasattr(c.args[0], 'table') and c.args[0].table.name == 'billion_ton_2023_record'),
        None
    )
    if record_call:
        stmt = record_call.args[0]
        params = stmt.compile().params
        assert "100" in str(params)
        assert "70.0" in str(params)
