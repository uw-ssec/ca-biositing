# PR: Land IQ ETL Normalization and Casing Fixes

## Overview

This PR addresses an issue where the Land IQ ETL pipeline was introducing
significant numbers of null values into the `landiq_record` table, particularly
for `dataset_id`, `main_crop`, and other crop-related columns. The root cause
was identified as a casing mismatch between the transformed data and the
database lookup tables, combined with a lack of automatic record creation for
new crops or datasets during the load process.

## Changes

### 1. Standardized Lowercasing Across Transformation Layer

To ensure consistency across the entire system, I have enforced lowercasing for
all primary agricultural product and resource names at the point of
transformation.

- **`primary_ag_product.py`**: Updated transformation logic to ensure all
  product names are lowercased and stripped of whitespace before being loaded
  into the lookup table.
- **`resource.py`**: Applied similar lowercasing and stripping logic to resource
  names.
- **`landiq_record.py`**: Updated the manual cleaning loop to lowercase all
  string-based columns, including `dataset` and all crop columns, to match the
  standardized lookup tables.

### 2. Robust "Get or Create" Logic in Load Step

Modified the Land IQ load task to be more resilient to new or inconsistently
cased data.

- **`load/landiq.py`**: Enhanced the `load_landiq_record` task to perform a "get
  or create" operation for both `Dataset` and `PrimaryAgProduct`. If a dataset
  (e.g., `landiq_2023`) or a crop name encountered in the Land IQ data does not
  exist in the database, it is now automatically created in lowercase. This
  ensures that foreign key lookups always return a valid ID, preventing nulls in
  the `landiq_record` table.

### 3. Data Integrity & Verification

- **Table Cleanup**: Coordinated a `TRUNCATE CASCADE` of affected tables
  (`landiq_record`, `polygon`, `dataset`, `primary_ag_product`, `resource`,
  etc.) to remove stale data and start from a clean, lowercased baseline.
- **Validation Run**: Successfully executed the full Land IQ ETL flow (446,713
  records). Verification via SQL confirmed:
  - **Zero nulls** in `dataset_id`.
  - **Zero nulls** in `main_crop`, `secondary_crop`, etc.
  - All crop names in `primary_ag_product` are consistently lowercased.

## Impact

These improvements eliminate the data quality issues previously seen in the Land
IQ dataset and establish a consistent casing standard for agricultural products
project-wide. The pipeline is now more autonomous, as it can self-populate
lookup tables when new crops are introduced in the source data.
