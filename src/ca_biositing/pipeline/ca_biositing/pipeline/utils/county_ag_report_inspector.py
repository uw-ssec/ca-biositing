"""
County Ag Report Column Inspector

Utility to inspect and display the actual column structure of the three
county ag report worksheets from Google Sheets.

Usage:
    pixi run python -m ca_biositing.pipeline.utils.county_ag_report_inspector

This will extract and print:
1. Column names from 07.7-Primary_products
2. Column names from 07.7a-PP_Prodn_Value (with wide format analysis)
3. Column names from 07.7b-PP_Data_sources
"""

import os
from prefect import flow
from ca_biositing.pipeline.etl.extract.factory import create_extractor


@flow(name="County Ag Report Column Inspection")
def inspect_county_ag_report_columns():
    """
    Extract and display all columns from the three county ag report worksheets.
    """
    GSHEET_NAME = "Aim 1-Feedstock Collection and Processing Data-BioCirV"

    # Ensure credentials.json is found if we're running from the root
    if os.path.exists("credentials.json"):
        os.environ["CREDENTIALS_PATH"] = os.path.abspath("credentials.json")

    print("=" * 80)
    print("COUNTY AG REPORT WORKSHEET COLUMN INSPECTION")
    print("=" * 80)

    # ===== Sheet 07.7: Primary Products =====
    print("\n" + "=" * 80)
    print("SHEET 1: 07.7-Primary_products")
    print("=" * 80)
    try:
        primary_products_extractor = create_extractor(GSHEET_NAME, "07.7-Primary_products")
        df_primary = primary_products_extractor()
        print(f"\nShape: {df_primary.shape[0]} rows × {df_primary.shape[1]} columns")
        print("\nColumn Names:")
        for i, col in enumerate(df_primary.columns, 1):
            print(f"  {i:2d}. {col!r}")
        print("\nFirst few rows (first 5 columns):")
        print(df_primary.iloc[:5, :5].to_string())
    except Exception as e:
        print(f"\nError extracting 07.7-Primary_products: {e}")

    # ===== Sheet 07.7a: Production/Value =====
    print("\n" + "=" * 80)
    print("SHEET 2: 07.7a-PP_Prodn_Value")
    print("=" * 80)
    try:
        pp_production_value_extractor = create_extractor(GSHEET_NAME, "07.7a-PP_Prodn_Value")
        df_pp_value = pp_production_value_extractor()
        print(f"\nShape: {df_pp_value.shape[0]} rows × {df_pp_value.shape[1]} columns")
        print("\nColumn Names:")
        for i, col in enumerate(df_pp_value.columns, 1):
            print(f"  {i:2d}. {col!r}")

        # Analyze wide format structure
        print("\n" + "-" * 80)
        print("WIDE FORMAT ANALYSIS")
        print("-" * 80)

        # Look for county-based column patterns
        prodn_cols = [col for col in df_pp_value.columns if "Prodn" in col]
        value_cols = [col for col in df_pp_value.columns if "Value" in col]

        print(f"\nProduction columns found: {len(prodn_cols)}")
        for col in prodn_cols:
            print(f"  - {col!r}")

        print(f"\nValue columns found: {len(value_cols)}")
        for col in value_cols:
            print(f"  - {col!r}")

        print(f"\nFirst few rows:")
        print(df_pp_value.head(5).to_string())

    except Exception as e:
        print(f"\nError extracting 07.7a-PP_Prodn_Value: {e}")

    # ===== Sheet 07.7b: Data Sources =====
    print("\n" + "=" * 80)
    print("SHEET 3: 07.7b-PP_Data_sources")
    print("=" * 80)
    try:
        pp_data_sources_extractor = create_extractor(GSHEET_NAME, "07.7b-PP_Data_sources")
        df_data_sources = pp_data_sources_extractor()
        print(f"\nShape: {df_data_sources.shape[0]} rows × {df_data_sources.shape[1]} columns")
        print("\nColumn Names:")
        for i, col in enumerate(df_data_sources.columns, 1):
            print(f"  {i:2d}. {col!r}")

        print("\nAll rows (data source reference table):")
        print(df_data_sources.to_string())

    except Exception as e:
        print(f"\nError extracting 07.7b-PP_Data_sources: {e}")

    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    inspect_county_ag_report_columns()
