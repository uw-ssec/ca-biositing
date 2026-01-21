"""
ETL Extract for Land IQ Data
---

This module provides functionality for extracting Land IQ geospatial data from shapefiles.
"""

import os
from typing import Optional
import geopandas as gpd
from prefect import task, get_run_logger

# --- CONFIGURATION ---
# Default path within the repository
# Note: Users must download the Land IQ shapefile from https://www.landiq.com/land-use-mapping
# and place it in the data/landiq/ directory.
DEFAULT_SHAPEFILE_PATH = "data/landiq/i15_Crop_Mapping_2023_Provisional.shp"

@task
def extract(shapefile_path: Optional[str] = None) -> Optional[gpd.GeoDataFrame]:
    """
    Extracts raw data from a Land IQ shapefile.

    This function serves as the 'Extract' step in an ETL pipeline for geospatial data.
    It uses geopandas to read the shapefile and returns a GeoDataFrame.

    Args:
        shapefile_path: Path to the Land IQ shapefile. If None, uses DEFAULT_SHAPEFILE_PATH.

    Returns:
        A geopandas GeoDataFrame containing the raw data, or None if an error occurs.
    """
    logger = get_run_logger()

    path = shapefile_path or DEFAULT_SHAPEFILE_PATH

    logger.info(f"Extracting Land IQ data from: {path}")

    if not os.path.exists(path):
        logger.error(f"Shapefile path does not exist: {path}")
        return None

    try:
        # Load the shapefile using geopandas
        gdf = gpd.read_file(path)

        if gdf is None or gdf.empty:
            logger.error(f"Extracted GeoDataFrame is empty or None from {path}")
            return None

        logger.info(f"Successfully extracted {len(gdf)} records from Land IQ shapefile.")
        logger.info(f"CRS: {gdf.crs}")

        return gdf

    except Exception as e:
        logger.error(f"Failed to extract Land IQ data: {e}", exc_info=True)
        return None
