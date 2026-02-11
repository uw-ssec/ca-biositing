# USDA ETL Pipeline Debugging Handoff Document

**Date:** February 10, 2026 **Branch:** `usda_etl_feat` **Issue:** USDA ETL
pipeline only succeeds for 4/17 commodities instead of all 17

## Problem Summary

The USDA ETL pipeline extracts data successfully for 15/16 commodities (10,060
records), but the **transform step silently filters out 6 specific fruit/nut
commodities**, resulting in only 9 commodities (4,165 records) making it to the
load step. Despite receiving properly mapped data, the load step inserts 0
records into the database.

## Root Cause Identified

**Transform step filtering** is the core bottleneck. The following 6 commodities
are being filtered out during transformation:

- PEACHES (240 records lost)
- ALMONDS (90 records lost)
- GRAPES (90 records lost)
- OLIVES (90 records lost)
- WALNUTS (90 records lost)
- PISTACHIOS (88 records lost)

Total lost: 598 records from these 6 commodities

## Data Flow Analysis (COMPLETED)

### Extract Step ✅ WORKING

- **Input:** 16 commodity codes from USDA NASS API
- **Output:** 15 commodities successfully extracted (10,060 records)
- **File:** `/data/usda_raw_extracted.csv` (mounted Docker volume, accessible on
  host)
- **Only failure:** 1 commodity fails API extraction (likely data unavailable)

### Transform Step ❌ FILTERING ISSUE

- **Input:** 15 commodities (10,060 records)
- **Output:** 9 commodities (4,165 records)
- **File:** `/data/usda_transformed_debug.csv`
- **Mapping Quality:** Perfect (0 null values for commodity_code, parameter_id,
  unit_id)
- **Issue:** Hidden filtering logic removes 6 specific commodities

### Load Step ❌ ZERO INSERTIONS

- **Input:** 9 commodities (4,165 records with perfect mapping)
- **Output:** 0 database insertions
- **Issue:** Despite receiving valid data, load step rejects all records

## Key Files & Locations

### Debug Data (Available Now)

- **Raw extract:**
  `c:\Users\meili\forked\ca-biositing\data\usda_raw_extracted.csv`
- **Transformed data:**
  `c:\Users\meili\forked\ca-biositing\data\usda_transformed_debug.csv`

### ETL Implementation

- **Transform:**
  `src/ca_biositing/pipeline/etl/transform/usda/usda_census_survey.py`
- **Load:** `src/ca_biositing/pipeline/etl/load/usda/usda_census_survey.py`
- **Flow:** `src/ca_biositing/pipeline/flows/usda/usda_census_survey.py`

## Infrastructure Status

### Database ✅ FIXED

- **Constraint Issue:** RESOLVED - Updated observation table to use 4-column
  unique constraint
- **Migration:** Applied via Alembic
- **Connection:** PostgreSQL on Docker port 5432 (external 9090)

### Docker Environment ✅ WORKING

- **Services:** Prefect + PostgreSQL running
- **Debug Access:** CSV files mounted to host via `/app/data` volume
- **Commands:**
  - Start: `pixi run start-services`
  - ETL: `pixi run run-etl`
  - Logs: `docker logs BioCirV_ETL_prefect_worker`

## Analysis Completed

### Commodity Breakdown (From CSV Analysis)

**Raw Extract (15 commodities, 10,060 records):**

- WHEAT: 5,134 records
- CORN: 1,358 records
- COTTON: 1,053 records
- RICE: 892 records
- HAY: 375 records
- TOMATOES: 326 records
- PEACHES: 240 records ❌ FILTERED OUT
- ALMONDS: 90 records ❌ FILTERED OUT
- GRAPES: 90 records ❌ FILTERED OUT
- OLIVES: 90 records ❌ FILTERED OUT
- WALNUTS: 90 records ❌ FILTERED OUT
- PISTACHIOS: 88 records ❌ FILTERED OUT
- Others: ~700 records (retained)

**Transformed Output (9 commodities, 4,165 records):**

- wheat: 2,256 records
- corn: 717 records
- rice: 394 records
- cotton: 301 records
- hay: 217 records
- tomatoes: 196 records
- cucumbers: 35 records
- sweet potatoes: 29 records
- potatoes: 20 records

### Mapping Analysis ✅ COMPLETED

- **Commodity mapping:** Working perfectly (0 nulls)
- **Parameter mapping:** Working perfectly (0 nulls)
- **Unit mapping:** Working perfectly (0 nulls)
- **Value conversion:** Working perfectly (0 nulls)

## Next Steps Required

### 1. **URGENT:** Identify Transform Filtering Logic

- **File:** `src/ca_biositing/pipeline/etl/transform/usda/usda_census_survey.py`
- **Question:** Why are PEACHES, ALMONDS, GRAPES, OLIVES, WALNUTS, PISTACHIOS
  filtered out?
- **Method:** Add debugging to transform step to log filtering decisions

### 2. Fix Transform Filtering

- Remove/modify filtering logic that excludes fruit/nut commodities
- Ensure all 15 extracted commodities pass through transform

### 3. Investigate Load Zero Insertions

- **File:** `src/ca_biositing/pipeline/etl/load/usda/usda_census_survey.py`
- **Current Issue:** 4,165 valid records → 0 insertions
- **Enhanced diagnostics:** Already added, need to review output

### 4. Post-Fix Tasks

- Update LinkML schema to remove record_id unique constraint
- Regenerate SQLAlchemy models
- Validate all 15 commodities working end-to-end

## Recent Diagnostic Enhancements

### Transform Step

- Added CSV debug output to `/app/data/usda_transformed_debug.csv`
- Added commodity mapping diagnostics
- Enhanced logging for filtering decisions

### Load Step

- Added detailed filtering diagnostics
- Enhanced logging for missing fields
- Added insertion success/failure tracking

## Commands for Debugging

```bash
# Run ETL with full diagnostics
pixi run run-etl

# Check container logs
docker logs BioCirV_ETL_prefect_worker

# Access debug CSV files
# Files are in: c:\Users\meili\forked\ca-biositing\data\

# Check service status
pixi run service-status

# Restart services if needed
pixi run start-services
```

## Key Insight

**The problem is NOT:**

- API extraction (works for 15/16 commodities)
- Database constraints (fixed)
- Data mapping (perfect quality)

**The problem IS:**

- Hidden filtering logic in transform step that specifically targets fruit/nut
  commodities
- Subsequent load issues (may resolve once transform fixed)

## Focus Area

**Start with transform step filtering logic** - this is where 6 commodities and
598 records are being silently dropped. Once this is fixed, the load step issues
may resolve automatically.

The pattern suggests intentional filtering of fruit/nut commodities vs.
grain/vegetable commodities, possibly based on:

- Commodity type classification
- Data validation rules
- Parameter/unit compatibility checks
- Value range filters

**Next agent should examine the transform function line-by-line to find this
filtering logic.**

## Status Update - February 10, 2026 ✅ FIXED

### Transform Issue RESOLVED

- **Root cause:** Fruit/nut commodities use different parameter types ("AREA
  BEARING" vs "AREA HARVESTED") and units ("OPERATIONS") not present in database
  mapping tables
- **Solution:** Added fruit-specific parameters and units to transform
  configuration
- **Result:** All 15 extracted commodities now process successfully (5,450
  records vs previous 4,165)
- **Verified:** Fruit/nut specific parameters now appear in observation table

### Load Step Working Correctly

- **"0 insertions" mystery solved:** Diagnostic reports only NEW insertions, not
  total records
- **Deduplication working:** ETL correctly skips records that already exist in
  database
- **Verified:** Database contains 241 census records, 799 survey records, 4,314
  observations

### Current ETL Performance

- **Extract:** 10,059 records → **Transform:** 5,450 records (54% success rate)
- **Transform → Load:** 1,040 parent records + 4,314 observations
- **Missing:** 1,136 observations (5,450 expected vs 4,314 actual)

## Known Issues & Future Improvements

### TO-DO: Database Schema Improvements

- **commodity_code field naming:** The field `commodity_code` in
  `usda_census_record` and `usda_survey_record` tables should be renamed to
  `commodity_id` for clarity, as it stores the integer ID that maps to
  `usda_commodity.usda_code` (text field). Currently requires casting
  (`commodity_code::text = usda_commodity.usda_code`) which is confusing.
  - **Risk:** Renaming may break existing queries/code
  - **Impact:** Improves data model clarity and removes need for type casting
  - **Priority:** Low (cosmetic improvement)

### TO-DO: Investigate Missing 1,136 Observations

- **Issue:** Transform outputs 5,450 records but only 4,314 observations loaded
- **Potential causes:** Failed parent record linking, validation failures,
  additional deduplication
- **Next steps:** Add enhanced load step diagnostics to track where observations
  are lost

### TO-DO: Enhanced Load Diagnostics

- Track records that fail parent record linking
- Log specific validation failures with examples
- Separate reporting for new vs skipped (deduplicated) records

### TO-DO: Database Constraint Improvements

- **Priority:** Medium (data integrity)
- **Missing Constraints:** Add unique constraints to prevent duplicates
- **Specific Changes:**

  ```sql
  -- Add unique constraint to usda_census_record
  ALTER TABLE usda_census_record
  ADD CONSTRAINT usda_census_record_unique
  UNIQUE (geoid, year, commodity_code);

  -- Add unique constraint to usda_survey_record
  ALTER TABLE usda_survey_record
  ADD CONSTRAINT usda_survey_record_unique
  UNIQUE (geoid, year, commodity_code);
  ```

- **Benefits:** Prevents duplicates from parallel ETL runs or manual insertion
- **Risk:** May fail if existing duplicates exist (but analysis shows 0
  duplicates currently)

### TO-DO: Data Type Consistency Cleanup

- **Priority:** Medium (schema consistency)
- **Issue:** Mixed data types for ID columns causing casting issues
- **Specific Changes:**
  - Change `observation.record_id` from `text` to `integer` (requires casting in
    queries currently)
  - Audit all `_id` columns for string vs integer inconsistencies
  - Update ETL load logic to use proper integer types
- **Benefits:** Eliminates need for `::integer` casting, improves query
  performance
- **Risk:** Requires schema migration and ETL code updates

### TO-DO: Code & Documentation Cleanup (Post-Debug)

- **Priority:** High (within next 2 hours)
- **Scope:** Clean up debugging outputs, code comments, and documentation
- **Tasks:**
  - Remove excessive diagnostic logging from transform step
  - Clean up emoji logging and temporary debug messages
  - Consolidate debug CSV files and analysis scripts
  - Update code documentation to reflect final solution
  - Remove temporary debugging code that's no longer needed
