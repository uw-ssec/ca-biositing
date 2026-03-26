import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from ca_biositing.pipeline.etl.transform.analysis.gasification_record import transform_gasification_record

@patch("ca_biositing.pipeline.etl.transform.analysis.gasification_record.get_run_logger")
@patch("ca_biositing.pipeline.etl.transform.analysis.gasification_record.normalize_dataframes")
def test_transform_gasification_record(mock_normalize, mock_logger):
    # Setup mock logger
    mock_logger.return_value = MagicMock()

    # Setup mock data for thermo_data
    # The flow now handles mapping to 'record_id'
    thermo_data_df = pd.DataFrame({
        "record_id": ["REC001", "REC001", "REC002"],
        "Experiment_id": ["EXP001", "EXP001", "EXP001"],
        "Parameter": ["Bio", "Ash", "Bio"],
        "Value": [10.5, 500.0, 12.0],
        "Resource": ["Rice Straw", "Rice Straw", "Rice Straw"],
        "Prepared_sample": ["RS-P1", "RS-P1", "RS-P1"],
        "Repl_no": ["1", "1", "1"],
        "raw_data_url": ["http://test.com", "http://test.com", "http://test.com"],
        "Note": ["Note 1", "Note 1", "Note 2"]
    })

    # Setup mock data for thermo_experiment
    thermo_experiment_df = pd.DataFrame({
        "Therm_exp_id": ["EXP001"],
        "Thermo_Exp_title": ["Test Gasification Exp"],
        "Method_id": ["M001"],
        "Reactor_id": ["R001"],
        "Analyst_email": ["test@example.com"]
    })

    # Setup mock normalization return
    def side_effect(dfs, columns):
        df = dfs[0].copy()
        for col in columns:
            if col in df.columns:
                df[f"{col}_id"] = 1 # Mock ID
        return [df]

    mock_normalize.side_effect = side_effect

    # Call the transform function
    result = transform_gasification_record.fn(
        thermo_data_df=thermo_data_df,
        thermo_experiment_df=thermo_experiment_df,
        etl_run_id=123,
        lineage_group_id=456
    )

    # Verify results
    assert not result.empty
    assert len(result) == 2 # REC001 and REC002 (duplicates dropped)
    assert "record_id" in result.columns
    assert "technical_replicate_no" in result.columns
    assert "note" in result.columns
    assert "etl_run_id" in result.columns
    assert "lineage_group_id" in result.columns

    # Check values for REC001 (standard_clean lowercases strings)
    rec001 = result[result["record_id"] == "rec001"].iloc[0]
    assert rec001["technical_replicate_no"] == 1
    assert rec001["note"] == "note 1"
    # Filter for columns that exist
    if "etl_run_id" in result.columns:
        assert rec001["etl_run_id"] == 123
    if "lineage_group_id" in result.columns:
        assert rec001["lineage_group_id"] == 456
