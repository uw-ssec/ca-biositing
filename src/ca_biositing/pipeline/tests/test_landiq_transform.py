import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from ca_biositing.pipeline.etl.transform.landiq.landiq_record import transform_landiq_record
from unittest.mock import MagicMock, patch

def test_transform_landiq_record_crop_mapping():
    # Create a dummy GeoDataFrame with crop codes
    data = {
        'UniqueID': ['1', '2'],
        'MAIN_CROP': ['G2', 'R1'],
        'CLASS1': ['F1', 'P1'],
        'CLASS2': ['T4', 'D1'],
        'CLASS3': ['C', 'V'],
        'CONFIDENCE': [1, 2],
        'geometry': [Point(0, 0), Point(1, 1)]
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # Mock the Prefect logger
    with patch('ca_biositing.pipeline.etl.transform.landiq.landiq_record.get_run_logger'):
        # Run the transform
        result_df = transform_landiq_record.fn(gdf)

        # Check if crop codes were converted to text and preserved (not normalized to IDs yet)
        assert 'main_crop' in result_df.columns
        assert result_df['main_crop'].iloc[0] == 'wheat' # lowercase because of the cleaning step
        assert result_df['main_crop'].iloc[1] == 'rice'

        assert 'secondary_crop' in result_df.columns
        assert result_df['secondary_crop'].iloc[0] == 'cotton'

        assert 'tertiary_crop' in result_df.columns
        assert result_df['tertiary_crop'].iloc[0] == 'cole crops'

        assert 'quaternary_crop' in result_df.columns
        assert result_df['quaternary_crop'].iloc[0] == 'citrus'

        assert 'confidence' in result_df.columns
        assert result_df['confidence'].iloc[0] == 1

        # Verify geometry is preserved for the load step
        assert 'geometry' in result_df.columns
        assert isinstance(result_df['geometry'].iloc[0], Point)

if __name__ == "__main__":
    test_transform_landiq_record_crop_mapping()
    print("Test passed!")
