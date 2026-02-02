import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.transform.field_sampling.field_sample import transform_field_sample
from sqlalchemy import Column, String, Integer

@patch("ca_biositing.pipeline.etl.transform.field_sampling.field_sample.normalize_dataframes")
def test_transform_field_sample(mock_normalize):
    # 1. Setup Mock Data
    metadata_raw = pd.DataFrame({
        "Field_Sample_Name": ["Pos-Alf033", "Pos-Alf033"],
        "Resource": ["Alfalfa", "Alfalfa"],
        "Provider_codename": ["possessive", "possessive"],
        "FV_Date_Time": ["6/30/2025 10:30", "6/30/2025 10:30"],
        "Sample_TS": ["6/30/2025 10:45", "6/30/2025 10:45"],
        "Qty": ["1", "1"],
        "Primary_Collector": ["Ziad Nasef", "Xihui Kang"],
        "Sample_Notes": ["Note 1", "Note 2"],
        "Sample_Source": ["Source A", "Source B"],
        "Prepared_Sample": ["Sample A", "Sample B"],
        "Storage_Mode": ["Method A", "Method B"]
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
    def side_effect(df, normalize_columns):
        df_norm = df.copy()
        df_norm["resource_id"] = 1
        df_norm["provider_codename_id"] = 10
        df_norm["primary_collector_id"] = 100
        df_norm["dataset_id"] = 500
        return df_norm

    mock_normalize.side_effect = side_effect

    # 3. Run Transform
    result_df = transform_field_sample.fn(data_sources, etl_run_id=123, lineage_group_id=456)

    # 4. Assertions
    assert result_df is not None
    assert not result_df.empty
    assert len(result_df) == 2

    # Check columns (using the rename_map names)
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
    assert row["dataset_id"] == 500
    assert row["etl_run_id"] == 123
    assert row["lineage_group_id"] == 456

if __name__ == "__main__":
    pytest.main([__file__])
