import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.transform.field_sampling.field_sample import transform_field_sample

@patch("ca_biositing.pipeline.etl.transform.field_sampling.field_sample.normalize_dataframes")
@patch("sqlmodel.Session")
@patch("ca_biositing.pipeline.utils.engine.engine")
def test_transform_field_sample(mock_engine, mock_session, mock_normalize):
    # 1. Setup Mock Data
    metadata_raw = pd.DataFrame({
        "Field_Sample_Name": ["Pos-Alf033", "Pos-Alf033", "Not-Core"],
        "Resource": ["Alfalfa", "Alfalfa", "Alfalfa"],
        "Provider_codename": ["possessive", "possessive", "possessive"],
        "FV_Date_Time": ["6/30/2025 10:30", "6/30/2025 10:30", "6/30/2025 10:30"],
        "Sample_TS": ["6/30/2025 10:45", "6/30/2025 10:45", "6/30/2025 10:45"],
        "Qty": ["1", "1", "1"],
        "Primary_Collector": ["Ziad Nasef", "Xihui Kang", "Someone Else"],
        "Sample_Notes": ["Note 1", "Note 2", "Note 3"],
        "Sample_Source": ["Source A", "Source B", "Source C"],
        "Prepared_Sample": ["Sample A", "Sample B", "Sample C"],
        "Storage_Mode": ["Method A", "Method B", "Method C"],
        "Sample_Unit": ["core", "Core", "not_core"],
        "County": ["San Joaquin", "San Joaquin", "San Joaquin"]
    })

    provider_raw = pd.DataFrame({
        "Provider_codename": ["possessive"],
        "County": ["San Joaquin"],
        "Primary_Ag_Product": ["Alfalfa"],
        "Provider_type": ["Farmer"],
        "Field_Storage_Location": ["Address A"]
    })

    data_sources = {
        "samplemetadata": metadata_raw,
        "provider_info": provider_raw
    }

    # 2. Mock normalize_dataframes to return a DF with expected ID columns
    def side_effect_normalize(df, normalize_columns):
        df_norm = df.copy()
        df_norm["resource_id"] = 1
        df_norm["provider_codename_id"] = 10
        df_norm["primary_collector_id"] = 100
        df_norm["dataset_id"] = 1
        return [df_norm]

    mock_normalize.side_effect = side_effect_normalize

    # 3. Mock Database Session
    mock_session_obj = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_session_obj

    # Mock Place lookup results
    mock_place = MagicMock()
    mock_place.geoid = "06077"
    mock_place.county_name = "San Joaquin"

    mock_exec = MagicMock()
    mock_session_obj.exec.return_value = mock_exec
    # The code calls .all() first for places, then .first() in a loop for LocationAddress
    mock_exec.all.return_value = [mock_place]
    mock_exec.first.return_value = MagicMock(id=1000)

    # 4. Run Transform
    result_df = transform_field_sample.fn(data_sources, etl_run_id=123, lineage_group_id=456)

    # 5. Assertions
    assert result_df is not None
    assert not result_df.empty
    # Deduplication based on field_sample_name
    assert len(result_df) == 2

    # Check columns
    assert "name" in result_df.columns
    assert "resource_id" in result_df.columns
    assert "provider_id" in result_df.columns
    assert "collector_id" in result_df.columns
    assert "sample_collection_source" in result_df.columns
    assert "collection_timestamp" in result_df.columns
    assert "dataset_id" in result_df.columns
    assert "etl_run_id" in result_df.columns

    # Check values
    row = result_df.iloc[0].to_dict()

    assert row["resource_id"] == 1
    assert row["provider_id"] == 10
    assert row["collector_id"] == 100
    assert row["dataset_id"] == 1
    assert row["etl_run_id"] == 123
    assert row["lineage_group_id"] == 456

def test_transform_field_sample_empty():
    data_sources = {"samplemetadata": pd.DataFrame(), "provider_info": pd.DataFrame()}
    result = transform_field_sample.fn(data_sources)
    assert result.empty

if __name__ == "__main__":
    pytest.main([__file__])
