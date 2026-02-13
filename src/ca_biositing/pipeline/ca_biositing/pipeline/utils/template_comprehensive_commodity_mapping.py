#!/usr/bin/env python3
"""
TEMPLATE: Comprehensive Commodity Mapping for Future Work

This file serves as a template/reference for the future comprehensive mapping
of all 465 USDA API commodities to our database commodities from the static website.

CURRENT STATUS: Template only - contains our original 17-commodity mapping logic
FUTURE USE: Starting point for comprehensive 465-commodity mapping system

See FUTURE_TODO_FULL_COMMODITY_MAPPING.md for implementation plan.
"""

from typing import Dict, Optional

# Official API name mappings based on our commodity analysis
DATABASE_TO_API_MAPPING: Dict[str, str] = {
    # Exact matches (no mapping needed, but listed for completeness)
    'ALMONDS': 'ALMONDS',
    'CUCUMBERS': 'CUCUMBERS',
    'OLIVES': 'OLIVES',
    'PEACHES': 'PEACHES',
    'TOMATOES': 'TOMATOES',
    'WHEAT': 'WHEAT',

    # Mappings needed for API compatibility
    'ALL GRAPES': 'GRAPES',
    'CORN  ALL': 'CORN',
    # NOTE: 'CORN FOR SILAGE' mapping kept for future expansion but not currently used
    # All current corn resources (including corn stover whole) map to 'CORN ALL'
    # CORN API response includes both grain and silage data automatically
    'CORN  FOR SILAGE': 'CORN',
    'COTTON  UPLAND': 'COTTON',
    'HAY  ALFALFA (DRY)': 'HAY',
    'PISTACHIO NUTS': 'PISTACHIOS',
    'POTATOES  ALL': 'POTATOES',
    'RICE  ALL': 'RICE',
    'SWEETPOTATOES': 'SWEET POTATOES',
    'TOMATOES FOR PROCESSING': 'TOMATOES',
    'WALNUTS (ENGLISH)': 'WALNUTS'
}

def get_api_name(database_name: str) -> str:
    """
    Get the official API commodity name for a database commodity name.

    Args:
        database_name: The commodity name as stored in our database

    Returns:
        The official API commodity name for USDA NASS QuickStats API
    """
    return DATABASE_TO_API_MAPPING.get(database_name, database_name)

def get_all_api_names() -> list[str]:
    """
    Get all unique API names that we use for API requests.

    Returns:
        List of unique API commodity names
    """
    return list(set(DATABASE_TO_API_MAPPING.values()))

def validate_mapping() -> Dict[str, str]:
    """
    Validate our mapping against known issues.

    Returns:
        Dict of any validation warnings
    """
    warnings = {}

    # Check for potential duplicates
    api_names = list(DATABASE_TO_API_MAPPING.values())
    duplicates = set([name for name in api_names if api_names.count(name) > 1])

    if duplicates:
        warnings['duplicate_api_names'] = f"Multiple database commodities map to: {duplicates}"

    # Check for common API name format issues
    for db_name, api_name in DATABASE_TO_API_MAPPING.items():
        if api_name.lower() != api_name.upper():  # Mixed case
            warnings[f'{db_name}_case'] = f"API name '{api_name}' has mixed case - verify with API"

    return warnings

if __name__ == "__main__":
    print("USDA COMMODITY API NAME MAPPING")
    print("=" * 40)

    print("Database Name → API Name:")
    for db_name, api_name in DATABASE_TO_API_MAPPING.items():
        marker = "✓" if db_name == api_name else "→"
        print(f"  {db_name:<25} {marker} {api_name}")

    print(f"\nTotal mappings: {len(DATABASE_TO_API_MAPPING)}")
    print(f"Unique API names: {len(set(DATABASE_TO_API_MAPPING.values()))}")

    # Validation
    warnings = validate_mapping()
    if warnings:
        print(f"\nValidation warnings:")
        for key, warning in warnings.items():
            print(f"  ⚠️  {warning}")
    else:
        print(f"\n✅ All mappings validated successfully")
