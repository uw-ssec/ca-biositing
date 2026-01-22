import pandas as pd
import pytest
from unittest.mock import MagicMock, patch
from ca_biositing.pipeline.etl.transform.resource import transform

# Mocking the database engine and session for normalize_dataframes
@patch("ca_biositing.pipeline.utils.engine.engine")
@patch("ca_biositing.pipeline.utils.name_id_swap.Session")
def test_resource_transform(mock_session, mock_engine):
    # 1. Setup Mock Data
    raw_data = pd.DataFrame({
        "Name": ["Almond Hulls", "Corn Stover"],
        "Resource Class": ["Agricultural Residue", "Agricultural Residue"],
        "Resource Subclass": ["Nut Hulls", "Cereal Straw"],
        "Primary Ag Product": ["Almonds", "Corn"],
        "Note": ["Test note 1", "Test note 2"],
        "Created At": ["2024-01-01", "2024-01-02"],
        "Updated At": ["2024-01-01", "2024-01-02"]
    })

    data_sources = {"basic_sample_info": raw_data}

    # 2. Mock DB responses for normalization
    mock_db = MagicMock()
    mock_session.return_value.__enter__.return_value = mock_db

    # Mocking the select results for each lookup table
    # This is a bit complex because normalize_dataframes calls replace_name_with_id_df multiple times
    def mock_execute(query):
        mock_result = MagicMock()
        # Extract the table name from the query to return appropriate mock data
        query_str = str(query)
        if "resource_class" in query_str:
            mock_result.all.return_value = [("agricultural residue", 1)]
        elif "resource_subclass" in query_str:
            mock_result.all.return_value = [("nut hulls", 10), ("cereal straw", 11)]
        elif "primary_ag_product" in query_str:
            mock_result.all.return_value = [("almonds", 100), ("corn", 101)]
        else:
            mock_result.all.return_value = []
        return mock_result

    mock_db.execute.side_effect = mock_execute

    # 3. Run Transform
    # We test the .fn() call which now handles the missing Prefect context gracefully
    result_df = transform.fn(data_sources, etl_run_id=1, lineage_group_id=10)

    # 4. Assertions
    assert result_df is not None
    assert not result_df.empty
    assert len(result_df) == 2

    # Check columns (normalized names)
    assert "name" in result_df.columns
    assert "resource_class_id" in result_df.columns
    assert "resource_subclass_id" in result_df.columns
    assert "primary_ag_product_id" in result_df.columns
    assert "etl_run_id" in result_df.columns

    # Check values
    assert result_df.iloc[0]["name"] == "almond hulls"
    assert result_df.iloc[0]["resource_class_id"] == 1
    assert result_df.iloc[0]["resource_subclass_id"] == 10
    assert result_df.iloc[0]["primary_ag_product_id"] == 100
    assert result_df.iloc[0]["etl_run_id"] == 1

if __name__ == "__main__":
    # Manual run if not using pytest
    try:
        test_resource_transform()
        print("Test PASSED")
    except Exception as e:
        print(f"Test FAILED: {e}")
        import traceback
        traceback.print_exc()
