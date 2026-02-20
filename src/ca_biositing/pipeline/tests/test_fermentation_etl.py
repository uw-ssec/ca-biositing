import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from prefect.testing.utilities import prefect_test_harness

# --- FERMENTATION ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.bioconversion_data.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.transform.analysis.observation.normalize_dataframes")
@patch("ca_biositing.pipeline.etl.transform.analysis.fermentation_record.normalize_dataframes")
@patch("ca_biositing.pipeline.etl.load.analysis.observation.engine")
@patch("ca_biositing.pipeline.etl.load.analysis.fermentation_record.engine")
def test_fermentation_etl_full(
    mock_engine,
    mock_obs_engine,
    mock_ferm_normalize,
    mock_obs_normalize,
    mock_gsheet,
):
    from ca_biositing.pipeline.etl.extract.bioconversion_data import extract
    from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
    from ca_biositing.pipeline.etl.load.analysis.fermentation_record import load_fermentation_record
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.load.analysis.observation import load_observation

    with prefect_test_harness():
        # 1. Mock Extract
        test_raw_df = pd.DataFrame({
            "UUID": ["uuid-1"],
            "Exp_ID": ["EXP_FERM_01"],
            "Name": ["Ferm_Test"],
            "Record_ID": ["FERM_001"],
            "created_at": ["2023-01-01"],
            "updated_at": ["2023-01-02"],
            "Method_ID": ["METH_01"],
            "Resource": ["Corn Stover"],
            "Prepared_sample": ["CS_PS_01"],
            "Well_position": ["B2"],
            "replicate_no": ["1"],
            "Parameter": ["Temperature"],
            "Value": ["37.0"],
            "Unit": ["C"],
            "qc_result": ["pass"],
            "analyst_email": ["analyst@example.com"],
            "inoculum_volume_L": ["0.05"],
            "reaction_volume_L": ["1.0"],
            "reactor_vessel": ["V-101"],
            "analysis_equipment": ["HPLC-01"],
            "raw_data_url": ["http://data.com/ferm001"],
            "note": ["No issues"]
        })
        mock_gsheet.return_value = test_raw_df

        # 2. Mock Transform Normalization
        mock_obs_normalize.return_value = pd.DataFrame({
            "dataset_id": [1],
            "analysis_type": ["fermentation"],
            "record_id": ["FERM_001"],
            "parameter_id": [1],
            "value": [37.0],
            "unit_id": [1],
            "note": ["test"],
            "etl_run_id": [1],
            "lineage_group_id": [1]
        })

        mock_ferm_normalize.return_value = pd.DataFrame({
            "record_id": ["FERM_001"],
            "replicate_no": [1],
            "well_position": ["B2"],
            "analyst_email_id": [10],
            "exp_id_id": [20],
            "method_id_id": [30],
            "reactor_vessel_id": [50],
            "analysis_equipment_id": [40],
            "raw_data_url_id": [100],
            "dataset_id": [1]
        })

        # 3. Mock Load
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_obs_engine.connect.return_value.__enter__.return_value = mock_conn

        # Execution
        raw_df = extract()

        # Observation path
        raw_df_obs = raw_df.copy()
        raw_df_obs['analysis_type'] = 'fermentation'
        obs_df = transform_observation([raw_df_obs])
        load_observation(obs_df)

        # Record path
        trans_df = transform_fermentation_record(raw_df)
        load_fermentation_record(trans_df)

        # Verification
        assert not raw_df.empty
        assert not obs_df.empty
        assert not trans_df.empty
        assert "record_id" in trans_df.columns
        assert "technical_replicate_no" in trans_df.columns
        assert "analyst_id" in trans_df.columns
        assert "experiment_id" in trans_df.columns
        assert "method_id" in trans_df.columns
        assert trans_df["method_id"].iloc[0] == 30
        assert "vessel_id" in trans_df.columns
        assert trans_df["vessel_id"].iloc[0] == 50

        # Verify columns removed
        assert "temperature" not in trans_df.columns
        assert "inoculum_volume_L" not in trans_df.columns
        assert "reaction_volume_L" not in trans_df.columns

        assert mock_gsheet.called
        assert mock_ferm_normalize.called
        assert mock_obs_normalize.called
        assert mock_engine.connect.called
        assert mock_obs_engine.connect.called
