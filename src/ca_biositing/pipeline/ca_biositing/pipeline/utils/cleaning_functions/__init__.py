"""Cleaning helpers package.

Expose commonly used cleaning and coercion helpers for the ETL pipeline.
This package is intentionally small and documented; individual modules contain
the implementation so unit tests can target them directly.
"""
from .cleaning import (
    clean_names_df,
    replace_empty_with_na,
    to_lowercase_df,
    standard_clean,
)

from .coercion import (
    coerce_columns,
    coerce_columns_list,
)

from .geospatial import (
    detect_latlon_columns,
    split_combined_latlon,
    standardize_latlon,
)

__all__ = [
    "clean_names_df",
    "replace_empty_with_na",
    "to_lowercase_df",
    "standard_clean",
    "coerce_columns",
    "coerce_columns_list",
    "detect_latlon_columns",
    "split_combined_latlon",
    "standardize_latlon",
]
