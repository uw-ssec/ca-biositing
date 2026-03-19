import pandas as pd
import pytest
from ca_biositing.pipeline.etl.transform.field_sampling.location_address import transform_location_address

def test_transform_location_address_basic():
    # 1. Setup Mock Data
    metadata_raw = pd.DataFrame({
        "sampling_location": ["San Joaquin", "San Joaquin", "Fresno"],
        "sampling_street": ["123 Main St", "123 Main St", None],
        "sampling_city": ["Stockton", "Stockton", "Fresno"],
        "sampling_zip": ["95202", "95202", "93701"]
    })

    data_sources = {
        "samplemetadata": metadata_raw
    }

    # 2. Run Transform
    result_df = transform_location_address.fn(data_sources, etl_run_id=123, lineage_group_id=456)

    # 3. Assertions
    assert result_df is not None
    assert not result_df.empty
    # Deduplication: 2 unique locations (123 Main St in Stockton, and anonymous in Fresno)
    assert len(result_df) == 2

    # Check columns
    assert "address_line1" in result_df.columns
    assert "city" in result_df.columns
    assert "zip" in result_df.columns
    assert "is_anonymous" in result_df.columns
    assert "etl_run_id" in result_df.columns
    assert "lineage_group_id" in result_df.columns

    # Verify is_anonymous logic (standard_clean lowercases strings)
    stockton = result_df[result_df['city'] == 'stockton'].iloc[0]
    assert stockton['is_anonymous'] == False
    assert stockton['address_line1'] == "123 main st"

    fresno = result_df[result_df['city'] == 'fresno'].iloc[0]
    assert fresno['is_anonymous'] == True
    assert fresno['address_line1'] is None or pd.isna(fresno['address_line1'])

def test_transform_location_address_empty():
    data_sources = {"samplemetadata": pd.DataFrame()}
    result = transform_location_address.fn(data_sources)
    assert result.empty

def test_transform_location_address_missing_source():
    data_sources = {}
    result = transform_location_address.fn(data_sources)
    assert result is None
