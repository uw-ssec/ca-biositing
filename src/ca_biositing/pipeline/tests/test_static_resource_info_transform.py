import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from ca_biositing.pipeline.etl.transform.resource_information.static_resource_info import transform_static_resource_info

@patch("ca_biositing.pipeline.etl.transform.resource_information.static_resource_info.normalize_dataframes")
def test_transform_static_resource_info(mock_normalize):
    # 1. Setup Mock Data matching the NEW specified columns
    raw_data = pd.DataFrame({
        "Resource": ["Corn", "Wheat", "Alfalfa"],
        "Resource Code": ["C1", "W1", "A1"],
        "LandIQ Crop Name": ["CORN_L", "WHEAT_L", "ALF_L"],
        "Residue Type": ["Stover", "Straw", "Hay"],
        "Collected?": ["Yes", "Yes", "No"],
        "From Month": ["1", "2", "3"],
        "To Month": ["10", "11", "12"],
        "Residue Yield (Wet Ton/Ac)": ["5.5", "3.2", "4.1"],
        "Moisture Content": ["15%", "12%", "10%"],
        "Residue Yield (Dry Ton/Ac)": ["4.67", "2.8", "3.69"]
    })

    data_sources = {
        "static_resource_info": raw_data
    }

    # 2. Mock normalize_dataframes
    def side_effect(df, normalize_columns):
        df_norm = df.copy()
        # Mock resource lookups
        df_norm["resource_id"] = [101, 102, 103]
        # Mock landiq_crop_name lookups (now normalized to PrimaryAgProduct)
        df_norm["landiq_crop_name_id"] = [1001, 1002, 1003]
        return df_norm

    mock_normalize.side_effect = side_effect

    # 3. Run Transform
    result = transform_static_resource_info.fn(data_sources, etl_run_id=123, lineage_group_id=456)

    # 4. Assertions
    assert "landiq_resource_mapping" in result
    assert "resource_availability" in result

    mapping_df = result["landiq_resource_mapping"]
    availability_df = result["resource_availability"]

    # Check LandIQ Mapping
    assert not mapping_df.empty
    assert len(mapping_df) == 3
    assert "landiq_crop_name" in mapping_df.columns
    assert "resource_id" in mapping_df.columns
    # Check that it uses the IDs from our mock
    assert mapping_df.iloc[0]["landiq_crop_name"] == 1001
    assert mapping_df.iloc[0]["resource_id"] == 101
    assert mapping_df.iloc[0]["etl_run_id"] == 123

    # Check Resource Availability
    assert not availability_df.empty
    assert len(availability_df) == 3
    assert "resource_id" in availability_df.columns
    assert "residue_factor_dry_tons_acre" in availability_df.columns
    assert "residue_factor_wet_tons_acre" in availability_df.columns
    assert "from_month" in availability_df.columns

    # Check values and types
    row = availability_df.iloc[0]
    assert row["resource_id"] == 101
    assert row["residue_factor_dry_tons_acre"] == 4.67
    assert row["residue_factor_wet_tons_acre"] == 5.5
    assert row["from_month"] == 1
    assert row["to_month"] == 10
    assert row["etl_run_id"] == 123

def test_transform_static_resource_info_empty():
    data_sources = {"static_resource_info": pd.DataFrame()}
    result = transform_static_resource_info.fn(data_sources)
    assert result["landiq_resource_mapping"].empty
    assert result["resource_availability"].empty

if __name__ == "__main__":
    pytest.main([__file__])
