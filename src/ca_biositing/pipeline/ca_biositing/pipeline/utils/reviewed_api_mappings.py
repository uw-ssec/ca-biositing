#!/usr/bin/env python3
"""
Reviewed and Approved API Name Mappings for USDA Commodities

This file contains the official mapping between database commodity names
and USDA NASS QuickStats API commodity names. These mappings have been
reviewed and approved for use in ETL processes.

DO NOT MODIFY without reviewing against the official API commodity list.
"""

from typing import Dict

# Reviewed and approved mappings
OFFICIAL_API_MAPPINGS: Dict[str, str] = {
    'ALL GRAPES': 'GRAPES',
    'ALMONDS': 'ALMONDS',
    'CORN  ALL': 'CORN',
    'CORN  FOR SILAGE': 'SILAGE',
    'COTTON  UPLAND': 'COTTON',
    'CUCUMBERS': 'CUCUMBERS',
    'HAY  ALFALFA (DRY)': 'HAY',
    'OLIVES': 'OLIVES',
    'PEACHES': 'PEACHES',
    'PISTACHIO NUTS': 'PISTACHIOS',
    'POTATOES  ALL': 'POTATOES',
    'RICE  ALL': 'RICE',
    'SWEETPOTATOES': 'SWEET POTATOES',
    'TOMATOES': 'TOMATOES',
    'TOMATOES FOR PROCESSING': 'TOMATOES',
    'WALNUTS (ENGLISH)': 'WALNUTS',
    'WHEAT': 'WHEAT',
}

def get_api_name(database_name: str) -> str:
    """
    Get the official API commodity name for a database commodity name.

    Args:
        database_name: The commodity name as stored in our database

    Returns:
        The official API commodity name for USDA NASS QuickStats API
    """
    return OFFICIAL_API_MAPPINGS.get(database_name, database_name)

def get_all_api_names() -> list[str]:
    """Get all unique API names that we use for API requests."""
    return list(set(OFFICIAL_API_MAPPINGS.values()))
