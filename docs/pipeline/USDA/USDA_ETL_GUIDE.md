# USDA ETL Pipeline Guide

**Component Documentation for USDA NASS API Integration**

**Last Updated**: February 10, 2026

## Overview

The USDA ETL pipeline extracts agricultural data from the USDA NASS QuickStats
API, transforms it for database storage, and loads it into PostgreSQL with full
deduplication and validation.

### 🔑 **Key Dependencies & Prerequisites**

The pipeline relies on a sophisticated **commodity mapping system** that bridges
our internal resource database with USDA API commodity names:

1. **Resource & Primary Ag Product Tables**: The system first checks the
   database for existing `resource` entries and `primary_ag_product` mappings
2. **Commodity Seeding**: If prerequisites aren't met (missing
   resources/products), the system automatically seeds the `usda_commodity`
   table from the backup CSV
3. **CSV Backup**: `commodity_mappings_corrected.csv` serves as the
   authoritative source for commodity mappings when database is empty
4. **Dynamic Fetching**: Once seeded, the `fetch_mapped_commodities` module
   dynamically queries mapped commodities from the database

This ensures the ETL can bootstrap itself on fresh databases while maintaining
data integrity on established systems.

## Pipeline Architecture

### 🏗️ **Component Structure**

```text
USDA ETL Pipeline Components:
├── 🔍 Prerequisites Check
│   ├── Database prerequisite validation (46+ resources, 18+ ag products)
│   ├── Commodity seeding from CSV backup (if needed)
│   └── Dynamic commodity fetching (fetch_mapped_commodities.py)
├── Extract (usda/usda_census_survey.py)
│   ├── API Configuration & Authentication (.env integration)
│   ├── Multi-year data fetching (1924-2024)
│   └── Debug CSV output (/data/usda_raw_extracted_debug_TIMESTAMP.csv)
├── Transform (usda/usda_census_survey.py)
│   ├── Geospatial ID normalization (FIPS codes)
│   ├── Commodity/Parameter/Unit mapping (database lookups)
│   ├── Data type conversion & cleaning
│   └── Debug CSV output (/data/usda_transformed_debug_TIMESTAMP.csv)
└── Load (usda/usda_census_survey.py)
    ├── Dataset creation & linking
    ├── 3-level deduplication strategy
    └── Parent record → Observation linking
```

### 🔗 **Data Flow**

1. **Extract**: API → Raw CSV (10,059 records typical)
2. **Transform**: Raw CSV → Cleaned CSV (5,450 records after filtering)
3. **Load**: Cleaned CSV → Database (2,564 unique observations + parent records)

## Key Components

### **🔍 Prerequisites & Commodity Mapping System**

**Purpose**: Ensure database has required resources and commodity mappings
before ETL execution

**Components**:

- **`seed_commodity_mappings.py`**: Seeds `usda_commodity` table from CSV backup
  when database is empty
- **`commodity_mappings_corrected.csv`**: Authoritative mapping source (40
  commodity mappings)
- **`fetch_mapped_commodities.py`**: Dynamic fetcher that queries database for
  mapped commodities
- **Prerequisite checks**: Validates 46+ resources and 18+ primary ag products
  exist

**Logic Flow**:

1. **Check Prerequisites**: Query database for required resources and ag
   products
2. **Conditional Seeding**: If prerequisites fail, automatically seed from CSV
   backup
3. **Commodity Fetching**: Dynamically fetch mapped commodities from seeded
   database
4. **ETL Execution**: Proceed with extract using fetched commodity list

This system ensures the ETL can bootstrap itself on fresh databases while
maintaining data integrity.

### **Extract Step**

- **Purpose**: Fetch data from USDA NASS QuickStats API
- **Output**: Raw CSV with all API fields (timestamped for debugging)
- **Key Features**:
  - Multi-commodity extraction (16 mapped commodities)
  - Multi-year coverage (1924-2024)
  - Automatic retry logic and error handling
  - Environment variable integration (.env file support)
  - Optional debug CSV generation with timestamps

### **Transform Step**

- **Purpose**: Clean and map raw data to database schema
- **Key Operations**:
  - FIPS code → geoid conversion
  - Commodity name → commodity_code mapping via `usda_commodity` table
  - Statistic description → parameter_id mapping via `parameter` table
  - Unit description → unit_id mapping via `unit` table
  - Data type conversion and validation
  - Fruit-specific parameter handling (AREA BEARING, AREA NON-BEARING)
- **Output**: Timestamped debug CSV for troubleshooting
- **Filtering**: Removes records without required fields or valid mappings

### **Load Step**

- **Purpose**: Insert data with deduplication
- **3-Level Deduplication**:
  1. **Level 1**: Query existing records from database
  2. **Level 2**: Skip duplicates within current batch
  3. **Level 3**: PostgreSQL `ON CONFLICT DO NOTHING`

## Database Integration

### **Tables Populated**

- `usda_census_record` - Census agricultural records
- `usda_survey_record` - Survey agricultural records
- `observation` - Individual measurements linked to records
- `dataset` - ETL run tracking and data lineage

### **Mapping Tables Used**

- `usda_commodity` - API commodity names → database commodity codes
- `parameter` - Statistic descriptions → parameter IDs
- `unit` - Unit descriptions → unit IDs

## Configuration

### **Commodity Support**

Currently supports 15+ commodities including:

- **Grains**: Corn, Wheat, Rice
- **Fiber**: Cotton (Upland)
- **Tree Nuts**: Almonds, Pistachios, Walnuts
- **Fruits**: Grapes, Peaches, Olives
- **Forage**: Alfalfa Hay

### **Parameter Types**

Supports diverse agricultural measurements:

- **Area**: Harvested, Planted, Bearing, Non-Bearing
- **Production**: Volume/weight outputs
- **Sales**: Number of operations
- **Chemical**: Compositional analysis (moisture, ash, lignin, etc.)

## Debugging & Operations

### **Debug Outputs**

- `usda_raw_extracted_debug_YYYYMMDD_HHMMSS.csv` - Raw API data with timestamp
- `usda_transformed_debug_YYYYMMDD_HHMMSS.csv` - Processed data ready for load
  with timestamp

**Note**: Debug CSV generation is **optional** and disabled by default. To
enable:

1. Uncomment debug blocks in extract/transform code
2. CSV files will include timestamps for tracking multiple runs
3. Re-comment blocks when debugging is complete

### **Testing & Validation Tools**

Located in `src/ca_biositing/pipeline/tests/USDA/`:

- **`test_usda_comprehensive.py`**: **⭐ RECOMMENDED** - Complete diagnostic
  suite for post-ETL validation. Best tool for checking database state after ETL
  run. Provides detailed analysis of:
  - ETL tracking tables (data_source, dataset counts)
  - USDA-specific database records (usda_census_record, usda_survey_record
    counts)
  - Parameters and units added by ETL
  - Commodity mappings with resource linkage
  - API connectivity verification
- **`test_seeding.py`**: Test commodity mapping seeding functionality
- **`test_api_names.py`**: Verify API commodity mappings and database
  connectivity
- **`test_usda_availability.py`**: Check USDA API data availability by
  commodity/county
- **SQL Scripts**: Various validation and diagnostic queries

**Database Connection**: All test scripts include automatic port fallback
(configured port → 5432) for compatibility across environments.

**💡 Post-ETL Validation Workflow**:

1. Run ETL: `pixi run run-etl`
2. Validate results:
   `pixi run python src/ca_biositing/pipeline/tests/USDA/test_usda_comprehensive.py`
3. Review comprehensive diagnostics output for data quality and completeness

### **Success Metrics**

- **Extract Success**: 15/16 commodities (94% success rate)
- **Transform Success**: ~54% raw records survive filtering
- **Load Success**: 100% of valid transformed records loaded
- **Database Seeding**: 40 commodity mappings, 16 USDA commodities

### **Common Issues**

- **API Rate Limits**: Handled with automatic retry and proper delays
- **Missing Mappings**: New parameters/units require database updates
- **Geoid Formatting**: Automatic FIPS code standardization
- **Port Configuration**: Database connection issues resolved with port fallback
- **Environment Variables**: `.env` file loading required for API keys

### **Environment Requirements**

- **USDA_NASS_API_KEY**: Required in `.env` file for API access
- **DATABASE_URL**: Optional, with automatic fallback to configured ports
- **python-dotenv**: Automatic environment variable loading
- **Database Prerequisites**: 46+ resources, 18+ primary ag products for full
  operation

## Monitoring

The pipeline provides detailed logging at key stages:

- Record counts at each step
- Mapping success rates
- Error reporting with context
- Performance timing

## Future Development TODOs

### **High Priority**

- **Database Schema Enhancements**:
  - Add UNIQUE constraint on `usda_commodity.usda_code` for better conflict
    handling
  - Add `created_at` and `updated_at` columns to `usda_commodity` table
  - Switch to `ON CONFLICT` clauses after adding constraints

### **Medium Priority**

- **Comprehensive Commodity Mapping** (See
  `FUTURE_TODO_FULL_COMMODITY_MAPPING.md`):
  - Expand from current 17 commodities to all 465 USDA NASS API commodities
  - Create categorization system for commodity types (crops, livestock,
    byproducts)
  - Build comprehensive mapping structure for broader agricultural analysis
  - Estimated effort: 1-2 days

### **Template Improvements**

- Update Google Sheets extraction templates to use actual sheet names
- Replace placeholder TODOs in template files with real configuration

For operational troubleshooting, see the
[USDA ETL Handoff Document](../../USDA_ETL_HANDOFF.md).
