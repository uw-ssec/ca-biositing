#!/usr/bin/env python3
"""
Data Exploration Script for SampleMetadata_v03-BioCirV

Inspects the four worksheets in the new Google Sheet and documents:
- Column names and data types
- Sample rows (first 5-10)
- Data quality issues (nulls, duplicates, inconsistencies)
- Summary statistics for each worksheet

Output: JSON and text reports to /exports directory for review.
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ca_biositing.pipeline.utils.gsheet_to_pandas import gsheet_to_df
from ca_biositing.pipeline.utils.gsheet_sheets import get_sheet_names


# Configuration
GSHEET_NAME = "SampleMetadata_v03-BioCirV"
WORKSHEETS = [
    "01_Sample_IDs",
    "02_Sample_Desc",
    "03_Qty_FieldStorage",
    "04_Producers",
]
EXPORTS_DIR = Path(__file__).parent.parent / "exports"
CREDENTIALS_PATH = "credentials.json"


def get_credentials_path() -> str:
    """
    Resolve the credentials path from environment or default location.
    """
    env_creds = os.getenv("CREDENTIALS_PATH")
    if env_creds:
        return env_creds

    # Try common locations
    for path in [CREDENTIALS_PATH, f"../{CREDENTIALS_PATH}", f"../../{CREDENTIALS_PATH}"]:
        if os.path.exists(path):
            return path

    return CREDENTIALS_PATH


def analyze_dataframe(df: pd.DataFrame, worksheet_name: str) -> Dict[str, Any]:
    """
    Analyze a single DataFrame and return metadata.
    """
    if df.empty:
        return {
            "worksheet": worksheet_name,
            "status": "EMPTY",
            "row_count": 0,
            "column_count": 0,
            "columns": [],
            "sample_rows": [],
        }

    analysis = {
        "worksheet": worksheet_name,
        "status": "OK",
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": [],
        "sample_rows": [],
        "null_counts": {},
        "duplicate_counts": {},
        "data_quality_issues": [],
    }

    # Column metadata
    for col in df.columns:
        col_info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notna().sum()),
            "null_count": int(df[col].isna().sum()),
            "null_percentage": round(100 * df[col].isna().sum() / len(df), 2),
            "unique_count": int(df[col].nunique()),
            "sample_values": df[col].dropna().head(3).tolist(),  # First 3 non-null values
        }
        analysis["columns"].append(col_info)
        analysis["null_counts"][col] = int(df[col].isna().sum())

    # Sample rows (first 5)
    sample_count = min(5, len(df))
    for idx in range(sample_count):
        row_dict = {}
        for col in df.columns:
            val = df.iloc[idx][col]
            # Convert non-serializable types to string
            if pd.isna(val):
                row_dict[col] = None
            elif isinstance(val, (str, int, float, bool)):
                row_dict[col] = val
            else:
                row_dict[col] = str(val)
        analysis["sample_rows"].append(row_dict)

    # Data quality issues

    # Check for duplicate rows
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        analysis["data_quality_issues"].append(
            f"Found {dup_count} duplicate rows"
        )

    # Check for completely empty columns
    empty_cols = [col for col in df.columns if df[col].isna().sum() == len(df)]
    if empty_cols:
        analysis["data_quality_issues"].append(
            f"Found {len(empty_cols)} completely empty columns: {empty_cols}"
        )

    # Check for high null percentage columns (>80%)
    high_null_cols = [
        col for col in df.columns
        if df[col].isna().sum() / len(df) > 0.8
    ]
    if high_null_cols:
        analysis["data_quality_issues"].append(
            f"Found {len(high_null_cols)} columns with >80% null values: {high_null_cols}"
        )

    return analysis


def main():
    """
    Main exploration workflow.
    """
    print(f"\n{'='*80}")
    print(f"Exploring: {GSHEET_NAME}")
    print(f"Credentials: {get_credentials_path()}")
    print(f"Output Directory: {EXPORTS_DIR}")
    print(f"{'='*80}\n")

    # Ensure exports directory exists
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Get credentials path
    creds_path = get_credentials_path()
    if not os.path.exists(creds_path):
        print(f"ERROR: Credentials file not found at {creds_path}")
        print("Please ensure credentials.json is in the root directory or CREDENTIALS_PATH is set.")
        sys.exit(1)

    # List available worksheets in the target sheet
    print("Fetching worksheet names from Google Sheet...")
    available_sheets = get_sheet_names(GSHEET_NAME, creds_path)
    if available_sheets is None:
        print(f"ERROR: Could not fetch sheet names. Check Google Sheet access.")
        sys.exit(1)

    print(f"Available worksheets: {available_sheets}\n")

    # Extract and analyze each worksheet
    all_analyses = []
    extraction_log = []

    for worksheet_name in WORKSHEETS:
        print(f"\nExtracting: {worksheet_name}...")
        try:
            df = gsheet_to_df(GSHEET_NAME, worksheet_name, creds_path)

            if df is None or df.empty:
                extraction_log.append({
                    "worksheet": worksheet_name,
                    "status": "EMPTY_OR_ERROR",
                    "error": "Extraction returned None or empty DataFrame"
                })
                print(f"  ⚠️  {worksheet_name} is empty or extraction failed")
                continue

            print(f"  ✓ Extracted {len(df)} rows, {len(df.columns)} columns")

            # Analyze the DataFrame
            analysis = analyze_dataframe(df, worksheet_name)
            all_analyses.append(analysis)

            extraction_log.append({
                "worksheet": worksheet_name,
                "status": "SUCCESS",
                "row_count": len(df),
                "column_count": len(df.columns),
            })

        except Exception as e:
            extraction_log.append({
                "worksheet": worksheet_name,
                "status": "ERROR",
                "error": str(e)
            })
            print(f"  ✗ Error extracting {worksheet_name}: {e}")

    # Generate text report
    text_report = generate_text_report(all_analyses, extraction_log)
    text_file = EXPORTS_DIR / f"sample_metadata_v03_exploration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(text_file, "w") as f:
        f.write(text_report)
    print(f"\n✓ Text report: {text_file}")

    # Generate JSON report
    json_report = {
        "timestamp": datetime.now().isoformat(),
        "gsheet_name": GSHEET_NAME,
        "extraction_log": extraction_log,
        "worksheets": all_analyses,
    }
    json_file = EXPORTS_DIR / f"sample_metadata_v03_exploration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(json_file, "w") as f:
        json.dump(json_report, f, indent=2, default=str)
    print(f"✓ JSON report: {json_file}")

    # Print summary
    print(f"\n{'='*80}")
    print("EXPLORATION SUMMARY")
    print(f"{'='*80}")
    for log_entry in extraction_log:
        status_icon = "✓" if log_entry["status"] == "SUCCESS" else "✗"
        print(f"{status_icon} {log_entry['worksheet']}: {log_entry['status']}")
        if "row_count" in log_entry:
            print(f"    Rows: {log_entry['row_count']}, Columns: {log_entry['column_count']}")

    print(f"\nExploration complete. Review reports for detailed findings.")
    print(f"{'='*80}\n")


def generate_text_report(analyses: List[Dict[str, Any]], extraction_log: List[Dict[str, Any]]) -> str:
    """
    Generate a human-readable text report of the exploration.
    """
    report = []
    report.append(f"{'='*100}")
    report.append(f"SampleMetadata_v03-BioCirV - Data Exploration Report")
    report.append(f"Generated: {datetime.now().isoformat()}")
    report.append(f"{'='*100}\n")

    # Extraction summary
    report.append("EXTRACTION SUMMARY")
    report.append("-" * 100)
    for entry in extraction_log:
        if entry["status"] == "SUCCESS":
            report.append(f"✓ {entry['worksheet']}: {entry['row_count']} rows, {entry['column_count']} columns")
        else:
            report.append(f"✗ {entry['worksheet']}: {entry.get('error', entry['status'])}")
    report.append("")

    # Detailed analysis per worksheet
    for analysis in analyses:
        report.append(f"\n{'='*100}")
        report.append(f"WORKSHEET: {analysis['worksheet']}")
        report.append(f"{'='*100}")

        if analysis["status"] == "EMPTY":
            report.append("(Empty worksheet - no data to analyze)")
            continue

        report.append(f"\nBasic Statistics:")
        report.append(f"  Total Rows: {analysis['row_count']}")
        report.append(f"  Total Columns: {analysis['column_count']}")

        # Column details
        report.append(f"\nColumns ({len(analysis['columns'])}):")
        report.append(f"{'-'*100}")
        report.append(f"{'Column Name':<30} {'Type':<15} {'Non-Null':<12} {'Unique':<10} {'Null %':<8} {'Sample Values':<30}")
        report.append(f"{'-'*100}")

        for col_info in analysis["columns"]:
            col_name = col_info["name"][:29]
            dtype = col_info["dtype"][:14]
            non_null = col_info["non_null_count"]
            unique = col_info["unique_count"]
            null_pct = col_info["null_percentage"]
            samples = ", ".join(str(v)[:20] for v in col_info["sample_values"][:2]) if col_info["sample_values"] else "N/A"

            report.append(f"{col_name:<30} {dtype:<15} {non_null:<12} {unique:<10} {null_pct:<8.1f} {samples:<30}")

        # Data quality issues
        if analysis.get("data_quality_issues"):
            report.append(f"\nData Quality Issues:")
            for issue in analysis["data_quality_issues"]:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append(f"\nData Quality: No major issues detected")

        # Sample rows
        report.append(f"\nSample Rows (first {len(analysis['sample_rows'])}):")
        report.append(f"{'-'*100}")
        for idx, row in enumerate(analysis["sample_rows"], 1):
            report.append(f"\nRow {idx}:")
            for col, val in row.items():
                report.append(f"  {col}: {val}")

    report.append(f"\n{'='*100}")
    report.append("END OF REPORT")
    report.append(f"{'='*100}")

    return "\n".join(report)


if __name__ == "__main__":
    main()
