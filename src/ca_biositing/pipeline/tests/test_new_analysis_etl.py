import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

# --- ICP ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.icp.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.extract.icp.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.analysis.icp_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.icp_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.icp_record.get_local_engine")
@patch("ca_biositing.pipeline.etl.transform.analysis.icp_record.normalize_dataframes")
def test_icp_etl_full(
    mock_normalize,
    mock_load_logger,
    mock_trans_logger,
    mock_ext_logger,
    mock_engine,
    mock_gsheet_to_df
):
    from ca_biositing.pipeline.etl.extract.icp import extract
    from ca_biositing.pipeline.etl.transform.analysis.icp_record import transform_icp_record
    from ca_biositing.pipeline.etl.load.analysis.icp_record import load_icp_record

    # 1. Mock Extract
    test_raw_df = pd.DataFrame({
        "record_id": ["ICP_001"],
        "repl_no": [1],
        "value": [10.5],
        "parameter": ["As"],
        "unit": ["mg/kg"],
        "raw_data_url": ["http://example.com/spec1"]
    })
    mock_gsheet_to_df.return_value = test_raw_df

    # 2. Mock Transform (normalize_dataframes needs to return a DF with expected columns)
    mock_normalize.return_value = pd.DataFrame({
        "record_id": ["ICP_001"],
        "repl_no": [1],
        "value": [10.5],
        "parameter_id": [1],
        "unit_id": [1],
        "dataset_id": [1],
        "raw_data_url_id": [100]
    })

    # 3. Mock Load
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    # Execution
    raw_df = extract.fn()
    trans_df = transform_icp_record.fn(raw_df)
    load_icp_record.fn(trans_df)

    # Verification
    assert not raw_df.empty
    assert not trans_df.empty
    assert "record_id" in trans_df.columns
    assert mock_gsheet_to_df.called
    assert mock_normalize.called
    assert "raw_data_id" in trans_df.columns
    assert trans_df["raw_data_id"].iloc[0] == 100
    assert mock_engine.called

# --- XRF ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.xrf.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.extract.xrf.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.analysis.xrf_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.xrf_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.xrf_record.get_local_engine")
@patch("ca_biositing.pipeline.etl.transform.analysis.xrf_record.normalize_dataframes")
def test_xrf_etl_full(
    mock_normalize,
    mock_load_logger,
    mock_trans_logger,
    mock_ext_logger,
    mock_engine,
    mock_gsheet_to_df
):
    from ca_biositing.pipeline.etl.extract.xrf import extract
    from ca_biositing.pipeline.etl.transform.analysis.xrf_record import transform_xrf_record
    from ca_biositing.pipeline.etl.load.analysis.xrf_record import load_xrf_record

    # 1. Mock Extract
    test_raw_df = pd.DataFrame({
        "record_id": ["XRF_001"],
        "repl_no": [1],
        "value": [5.2],
        "wavelength_nm": [0.154],
        "intensity": [1000],
        "raw_data_url": ["http://example.com/spec1"]
    })
    mock_gsheet_to_df.return_value = test_raw_df

    # 2. Mock Transform
    mock_normalize.return_value = pd.DataFrame({
        "record_id": ["XRF_001"],
        "repl_no": [1],
        "value": [5.2],
        "wavelength_nm": [0.154],
        "intensity": [1000],
        "dataset_id": [1],
        "raw_data_url_id": [101]
    })

    # 3. Mock Load
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    # Execution
    raw_df = extract.fn()
    trans_df = transform_xrf_record.fn(raw_df)
    load_xrf_record.fn(trans_df)

    # Verification
    assert not raw_df.empty
    assert not trans_df.empty
    assert "wavelength_nm" in trans_df.columns
    assert "raw_data_id" in trans_df.columns
    assert trans_df["raw_data_id"].iloc[0] == 101
    assert mock_gsheet_to_df.called

# --- CALORIMETRY ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.calorimetry.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.extract.calorimetry.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.analysis.calorimetry_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.calorimetry_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.calorimetry_record.get_local_engine")
@patch("ca_biositing.pipeline.etl.transform.analysis.calorimetry_record.normalize_dataframes")
def test_calorimetry_etl_full(
    mock_normalize,
    mock_load_logger,
    mock_trans_logger,
    mock_ext_logger,
    mock_engine,
    mock_gsheet_to_df
):
    from ca_biositing.pipeline.etl.extract.calorimetry import extract
    from ca_biositing.pipeline.etl.transform.analysis.calorimetry_record import transform_calorimetry_record
    from ca_biositing.pipeline.etl.load.analysis.calorimetry_record import load_calorimetry_record

    # 1. Mock Extract
    test_raw_df = pd.DataFrame({
        "record_id": ["CAL_001"],
        "repl_no": [1],
        "value": [20.5],
        "parameter": ["HHV"]
    })
    mock_gsheet_to_df.return_value = test_raw_df

    # 2. Mock Transform
    mock_normalize.return_value = pd.DataFrame({
        "record_id": ["CAL_001"],
        "repl_no": [1],
        "value": [20.5],
        "parameter_id": [1],
        "dataset_id": [1]
    })

    # 3. Mock Load
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    # Execution
    raw_df = extract.fn()
    trans_df = transform_calorimetry_record.fn(raw_df)
    load_calorimetry_record.fn(trans_df)

    # Verification
    assert not raw_df.empty
    assert not trans_df.empty
    assert "record_id" in trans_df.columns
    assert mock_gsheet_to_df.called

# --- XRD ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.xrd.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.extract.xrd.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.analysis.xrd_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.xrd_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.load.analysis.xrd_record.get_local_engine")
@patch("ca_biositing.pipeline.etl.transform.analysis.xrd_record.normalize_dataframes")
def test_xrd_etl_full(
    mock_normalize,
    mock_load_logger,
    mock_trans_logger,
    mock_ext_logger,
    mock_engine,
    mock_gsheet_to_df
):
    from ca_biositing.pipeline.etl.extract.xrd import extract
    from ca_biositing.pipeline.etl.transform.analysis.xrd_record import transform_xrd_record
    from ca_biositing.pipeline.etl.load.analysis.xrd_record import load_xrd_record

    # 1. Mock Extract
    test_raw_df = pd.DataFrame({
        "record_id": ["XRD_001"],
        "repl_no": [1],
        "scan_low_nm": [10],
        "scan_high_nm": [90]
    })
    mock_gsheet_to_df.return_value = test_raw_df

    # 2. Mock Transform
    mock_normalize.return_value = pd.DataFrame({
        "record_id": ["XRD_001"],
        "repl_no": [1],
        "scan_low_nm": [10],
        "scan_high_nm": [90],
        "dataset_id": [1]
    })

    # 3. Mock Load
    mock_conn = MagicMock()
    mock_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

    # Execution
    raw_df = extract.fn()
    trans_df = transform_xrd_record.fn(raw_df)
    load_xrd_record.fn(trans_df)

    # Verification
    assert not raw_df.empty
    assert not trans_df.empty
    assert "scan_low_nm" in trans_df.columns
    assert "scan_high_nm" in trans_df.columns
    assert mock_gsheet_to_df.called
