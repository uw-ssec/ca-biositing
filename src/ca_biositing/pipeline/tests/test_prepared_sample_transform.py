import pandas as pd
import pytest
from unittest.mock import patch
from ca_biositing.pipeline.etl.transform.prepared_sample import transform

def test_prepared_sample_transform():
    # 1. Setup Mock Data
    preparation_raw = pd.DataFrame({
        "Prepared_Sample": ["Prep-001", "Prep-002"],
        "Sample_Name": ["Field-001", "Field-002"],
        "Preparation_Method": ["Grinding", "Drying"],
        "Preparation_Date": ["2024-01-01", "2024-01-02"],
        "Analyst_Email": ["analyst1@example.com", "analyst2@example.com"],
        "Prep_Temp_C": ["25", "60"],
        "Amount_Before_Drying_G": ["100.5", "200.0"],
        "Drying_Step": ["No", "Yes"],
        "Note": ["Note 1", "Note 2"]
    })

    data_sources = {
        "preparation": preparation_raw
    }

    # 2. Mock normalize_dataframes to return a DF with expected ID columns
    with patch("ca_biositing.pipeline.etl.transform.prepared_sample.normalize_dataframes") as mock_normalize:
        def side_effect(df, normalize_columns):
            df_norm = df.copy()
            df_norm["sample_name_id"] = [10, 20]
            df_norm["preparation_method_id"] = [100, 200]
            df_norm["analyst_email_id"] = [1000, 2000]
            return df_norm

        mock_normalize.side_effect = side_effect

        # 3. Run Transform
        result_df = transform.fn(data_sources, etl_run_id=123, lineage_group_id=456)

        # 4. Assertions
        assert result_df is not None
        assert not result_df.empty
        assert len(result_df) == 2

        # Check columns (using the rename_map names)
        assert "name" in result_df.columns
        assert "field_sample_id" in result_df.columns
        assert "prep_method_id" in result_df.columns
        assert "prep_date" in result_df.columns
        assert "preparer_id" in result_df.columns
        assert "note" in result_df.columns
        assert "etl_run_id" in result_df.columns
        assert "lineage_group_id" in result_df.columns

        # Check values
        row = result_df.iloc[0].to_dict()
        assert row["name"] == "prep-001"
        assert row["field_sample_id"] == 10
        assert row["prep_method_id"] == 100
        assert row["preparer_id"] == 1000
        assert row["etl_run_id"] == 123
        assert row["lineage_group_id"] == 456

if __name__ == "__main__":
    pytest.main([__file__])
