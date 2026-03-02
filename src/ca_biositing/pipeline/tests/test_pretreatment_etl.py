import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from prefect.testing.utilities import prefect_test_harness

# --- PRETREATMENT ETL TEST ---
@patch("ca_biositing.pipeline.etl.extract.pretreatment_data.gsheet_to_df")
@patch("ca_biositing.pipeline.etl.transform.analysis.observation.normalize_dataframes")
@patch("ca_biositing.pipeline.etl.transform.analysis.pretreatment_record.normalize_dataframes")
@patch("ca_biositing.pipeline.etl.load.analysis.observation.get_engine")
@patch("ca_biositing.pipeline.etl.load.analysis.pretreatment_record.engine")
def test_pretreatment_etl_full(
    mock_engine,
    mock_get_engine,
    mock_prec_normalize,
    mock_obs_normalize,
    mock_gsheet,
):
    from ca_biositing.pipeline.etl.extract.pretreatment_data import extract
    from ca_biositing.pipeline.etl.transform.analysis.pretreatment_record import transform_pretreatment_record
    from ca_biositing.pipeline.etl.load.analysis.pretreatment_record import load_pretreatment_record
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.load.analysis.observation import load_observation

    with prefect_test_harness():
        # 1. Mock Extract
        test_raw_df = pd.DataFrame({
            "Record_id": ["PRETREAT_001"],
            "Repl_number": [1],
            "Block_position": ["A1"],
            "Parameter": ["Temperature"],
            "Value": ["120.5"],
            "Analyst_email": ["test@example.com"],
            "Pretreatment_exper_name": ["Exp_1"],
            "Decon_method_id": ["Method_A"],
            "EH_method_id": ["EH_Method_X"],
            "Vessel_id": ["Rea-001"],
            "Reaction_block_id": ["Block_1"],
            "Raw_data_url": ["http://example.com/data"]
        })
        mock_gsheet.return_value = test_raw_df

        # 2. Mock Transform
        mock_obs_normalize.return_value = pd.DataFrame({
            "dataset_id": [1],
            "analysis_type": ["pretreatment"],
            "record_id": ["PRETREAT_001"],
            "parameter_id": [1],
            "value": [120.5],
            "unit_id": [1],
            "note": ["test"],
            "etl_run_id": [1],
            "lineage_group_id": [1]
        })

        mock_prec_normalize.return_value = pd.DataFrame({
            "record_id": ["PRETREAT_001"],
            "repl_number": [1],
            "block_position": ["A1"],
            "temperature": [120.5],
            "analyst_email_id": [10],
            "pretreatment_exper_name_id": [20],
            "decon_method_id_id": [30],
            "eh_method_id_id": [35],
            "vessel_id_id": [50],
            "reaction_block_id_id": [40],
            "raw_data_url_id": [100],
            "dataset_id": [1]
        })

        # 3. Mock Load
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_get_engine.return_value.connect.return_value.__enter__.return_value = mock_conn

        # Execution - Calling without .fn() to trigger task orchestration
        raw_df = extract()

        # Observation path
        raw_df_obs = raw_df.copy()
        raw_df_obs['analysis_type'] = 'pretreatment'
        obs_df = transform_observation([raw_df_obs])
        load_observation(obs_df)

        # Record path
        trans_df = transform_pretreatment_record(raw_df)
        load_pretreatment_record(trans_df)

        # Verification
        assert not raw_df.empty
        assert not obs_df.empty
        assert not trans_df.empty
        assert "record_id" in trans_df.columns
        assert "replicate_no" in trans_df.columns
        assert "temperature" in trans_df.columns
        assert "analyst_id" in trans_df.columns
        assert "pretreatment_method_id" in trans_df.columns
        assert "eh_method_id" in trans_df.columns
        assert trans_df["eh_method_id"].iloc[0] == 35
        assert "vessel_id" in trans_df.columns
        assert trans_df["vessel_id"].iloc[0] == 50
        assert trans_df["temperature"].iloc[0] == 120.5
        assert mock_gsheet.called
        assert mock_prec_normalize.called
        assert mock_obs_normalize.called
        assert mock_engine.connect.called
        assert mock_get_engine.called
