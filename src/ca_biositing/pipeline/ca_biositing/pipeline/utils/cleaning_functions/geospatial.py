"""Geospatial data cleaning helpers: latitude/longitude parsing and standardization."""
from typing import Iterable, Optional, Dict, Tuple
import logging
import re
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


# Regex patterns for detecting lat/lon column names
LAT_PATTERNS = [
    r"^desc_lat$",
    r"^latitude$",
    r"^lat$",
    r".*_lat$",
    r"^lat_.*",
]
LON_PATTERNS = [
    r"^desc_lon$",
    r"^longitude$",
    r"^lon$",
    r".*_lon$",
    r"^lon_.*",
]
COMBINED_PATTERNS = [
    r".*latlong.*",
    r".*lat_lon.*",
    r".*latitude_longitude.*",
    r".*latlng.*",
    r".*location.*",
    r".*coordinates.*",
]


def _matches_patterns(col_name: str, patterns: Iterable[str], case_insensitive: bool = True) -> bool:
    """Check if column name matches any pattern in the list."""
    col_lower = col_name.lower() if case_insensitive else col_name
    for pattern in patterns:
        if re.match(pattern, col_lower, re.IGNORECASE if case_insensitive else 0):
            return True
    return False


def detect_latlon_columns(df: pd.DataFrame) -> Dict[str, list]:
    """Auto-detect latitude and longitude columns in a DataFrame.

    Searches for common naming patterns like:
    - latitude/longitude, lat/lon, desc_lat/desc_lon
    - sampling_lat/sampling_lon, prod_lat/prod_lon, etc.
    - Combined columns: latlong, lat_lon, latlng, location, coordinates

    Returns:
        Dict with keys:
        - 'latitude': list of detected latitude columns
        - 'longitude': list of detected longitude columns
        - 'combined': list of combined lat/lon columns
    """
    result = {"latitude": [], "longitude": [], "combined": []}

    for col in df.columns:
        col_lower = col.lower()

        # Check combined patterns first
        if _matches_patterns(col, COMBINED_PATTERNS):
            result["combined"].append(col)
            logger.info(f"Detected combined lat/lon column: '{col}'")
        # Check latitude patterns
        elif _matches_patterns(col, LAT_PATTERNS):
            result["latitude"].append(col)
            logger.info(f"Detected latitude column: '{col}'")
        # Check longitude patterns
        elif _matches_patterns(col, LON_PATTERNS):
            result["longitude"].append(col)
            logger.info(f"Detected longitude column: '{col}'")

    return result


def _parse_latlon_pair(value: str, sep: Optional[str] = None) -> Tuple[Optional[float], Optional[float]]:
    """Parse a single lat/lon pair from a string.

    Tries multiple delimiters if sep not specified: comma, space, semicolon, pipe.
    Returns tuple (lat, lon) or (None, None) if parsing fails.
    """
    if not isinstance(value, str) or not value.strip():
        return None, None

    value = value.strip()
    parts = None

    # If separator specified, use it
    if sep:
        parts = [p.strip() for p in value.split(sep)]
    else:
        # Try common delimiters in order
        for delimiter in [",", ";", "|", "\t"]:
            if delimiter in value:
                parts = [p.strip() for p in value.split(delimiter)]
                break

        # If no delimiter found, try space (last resort)
        if parts is None or len(parts) == 1:
            parts = value.split()

    # Extract lat and lon
    if len(parts) >= 2:
        try:
            lat = float(parts[0])
            lon = float(parts[1])
            return lat, lon
        except (ValueError, IndexError):
            logger.warning(f"Could not parse lat/lon from: '{value}'")
            return None, None

    return None, None


def split_combined_latlon(
    df: pd.DataFrame,
    col: str,
    sep: Optional[str] = None,
    lat_col: str = "desc_lat",
    lon_col: str = "desc_lon",
    keep_original: bool = False,
) -> pd.DataFrame:
    """Split a combined lat/lon column into two separate columns.

    Handles multiple separators: comma, space, semicolon, pipe, tab.
    Auto-detects delimiter if not specified.

    Args:
        df: input DataFrame
        col: name of combined lat/lon column
        sep: delimiter (e.g., ',', ';'); if None, auto-detects
        lat_col: name for output latitude column
        lon_col: name for output longitude column
        keep_original: if True, keep the original combined column

    Returns:
        DataFrame with new lat/lon columns
    """
    if col not in df.columns:
        logger.warning(f"Column '{col}' not found in DataFrame")
        return df

    df = df.copy()
    logger.info(f"Splitting combined lat/lon column '{col}' into '{lat_col}' and '{lon_col}'")

    # Parse each value
    lats = []
    lons = []
    for idx, value in enumerate(df[col]):
        lat, lon = _parse_latlon_pair(value, sep=sep)
        lats.append(lat)
        lons.append(lon)
        if lat is None or lon is None:
            logger.debug(f"Row {idx}: could not parse '{value}'")

    # Create new columns
    df[lat_col] = pd.array(lats, dtype="float64")
    df[lon_col] = pd.array(lons, dtype="float64")

    # Optionally remove original
    if not keep_original:
        df = df.drop(columns=[col])
        logger.info(f"Dropped original column '{col}'")

    non_null_count = sum(1 for lat, lon in zip(lats, lons) if lat is not None and lon is not None)
    logger.info(f"Successfully parsed {non_null_count}/{len(lats)} lat/lon pairs")

    return df


def standardize_latlon(
    df: pd.DataFrame,
    lat_cols: Optional[Iterable[str]] = None,
    lon_cols: Optional[Iterable[str]] = None,
    combined_cols: Optional[Iterable[str]] = None,
    auto_detect: bool = True,
    output_lat: str = "desc_lat",
    output_lon: str = "desc_lon",
    sep: Optional[str] = None,
    coerce_to_float: bool = True,
) -> pd.DataFrame:
    """Standardize latitude/longitude columns in a DataFrame.

    Workflow:
    1. Auto-detect lat/lon columns if enabled
    2. Split any combined lat/lon columns
    3. Rename detected separate columns to output names
    4. Optionally coerce to float with error handling

    Args:
        df: input DataFrame
        lat_cols: explicit list of latitude columns to process
        lon_cols: explicit list of longitude columns to process
        combined_cols: explicit list of combined lat/lon columns to split
        auto_detect: if True, automatically detect columns by name pattern
        output_lat: name for standardized latitude column
        output_lon: name for standardized longitude column
        sep: delimiter for parsing combined columns
        coerce_to_float: if True, coerce to float64

    Returns:
        DataFrame with standardized lat/lon columns
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("standardize_latlon: input is not a DataFrame")
        return df

    df = df.copy()

    # Auto-detect if enabled
    if auto_detect:
        detected = detect_latlon_columns(df)
        lat_cols = lat_cols or detected.get("latitude", [])
        lon_cols = lon_cols or detected.get("longitude", [])
        combined_cols = combined_cols or detected.get("combined", [])
    else:
        lat_cols = lat_cols or []
        lon_cols = lon_cols or []
        combined_cols = combined_cols or []

    # Split combined columns first
    for col in combined_cols:
        if col in df.columns:
            df = split_combined_latlon(df, col, sep=sep, lat_col=output_lat, lon_col=output_lon, keep_original=False)

    # Handle separate lat/lon columns
    # If we have separate columns, merge them into the output columns
    # BUT: skip if we already created output columns from combined columns
    if (lat_cols or lon_cols) and output_lat not in df.columns and output_lon not in df.columns:
        # Use first available columns (could be extended for multiple lat/lon pairs)
        lat_cols = list(lat_cols) if lat_cols else []
        lon_cols = list(lon_cols) if lon_cols else []

        lat_col_to_use = next((c for c in lat_cols if c in df.columns), None)
        lon_col_to_use = next((c for c in lon_cols if c in df.columns), None)

        rename_dict = {}
        if lat_col_to_use:
            rename_dict[lat_col_to_use] = output_lat
        if lon_col_to_use:
            rename_dict[lon_col_to_use] = output_lon

        if rename_dict:
            logger.info(f"Standardizing columns: {rename_dict}")
            df = df.rename(columns=rename_dict)
        else:
            if lat_cols:
                logger.warning(f"Latitude columns specified {lat_cols} but not found in DataFrame")
            if lon_cols:
                logger.warning(f"Longitude columns specified {lon_cols} but not found in DataFrame")

    # Coerce to float if requested
    if coerce_to_float:
        for col in [output_lat, output_lon]:
            if col in df.columns and df[col] is not None:
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")
                    null_count = df[col].isnull().sum()
                    if null_count > 0:
                        logger.warning(f"Column '{col}': {null_count} values could not be coerced to float")
                except Exception as e:
                    logger.warning(f"Could not coerce '{col}' to float: {e}")

    return df
