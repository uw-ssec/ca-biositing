# USDA ETL Testing and Diagnostics

This directory contains SQL scripts and Python tools for testing and diagnosing
the USDA ETL pipeline.

## Database Connection Setup

The database runs in a **Docker container** but is accessible from your **local
machine**:

### Architecture

```
Local Machine (Configured Port) → Docker Container (Port 5432)
     ↑                                    ↑
Your SQL Client                    PostgreSQL Database
```

### Connection Details

- **Container Service**: `BioCirV_ETL_db` (PostgreSQL with PostGIS)
- **Local Access Port**: Configured in `resources/docker/.env` (typically
  `POSTGRES_PORT`)
- **Container Internal Port**: `5432` (standard PostgreSQL)
- **Database Name**: `biocirv_db`
- **Username**: `biocirv_user`
- **Password**: `biocirv_dev_password`

## How to Run SQL Scripts

### Method 1: Using psql Command Line

```bash
# Make sure Docker services are running
pixi run start-services

# Check configured port in resources/docker/.env
cat resources/docker/.env | grep POSTGRES_PORT

# Connect to database (use the configured port)
psql -h localhost -p $POSTGRES_PORT -U biocirv_user -d biocirv_db

# Run a specific SQL file
\i src/ca_biositing/pipeline/tests/USDA/check_etl_summary.sql

# Or run directly from command line
psql -h localhost -p $POSTGRES_PORT -U biocirv_user -d biocirv_db -f src/ca_biositing/pipeline/tests/USDA/check_etl_summary.sql
```

### Method 2: Using Database GUI Tools

**Connection Parameters:**

- Host: `localhost`
- Port: Check `POSTGRES_PORT` in `resources/docker/.env` (commonly `5432` or
  custom)
- Database: `biocirv_db`
- Username: `biocirv_user`
- Password: `biocirv_dev_password`

**Compatible Tools:**

- DBeaver
- pgAdmin
- TablePlus
- DataGrip
- VS Code PostgreSQL extension

### Method 3: Using Python Scripts

The Python test scripts in this directory already handle database connectivity:

```bash
# Run with automatic port fallback
pixi run python src/ca_biositing/pipeline/tests/USDA/test_api_names.py
pixi run python src/ca_biositing/pipeline/tests/USDA/test_seeding.py
```

## Port Troubleshooting

If you can't connect, check your configured port:

```bash
# Check what port is configured
cat resources/docker/.env | grep POSTGRES_PORT

# Check what ports are actually in use
pixi run service-status

# Try standard PostgreSQL port as fallback
psql -h localhost -p 5432 -U biocirv_user -d biocirv_db
```

**Common Scenarios:**

- **Custom Port**: Configured in `resources/docker/.env` as `POSTGRES_PORT`
- **Standard Port 5432**: If using default PostgreSQL configuration
- **Connection refused**: Database container isn't running → run
  `pixi run start-services`

## SQL Scripts Reference

### Data Validation Scripts

| Script                       | Purpose                       | When to Use                    |
| ---------------------------- | ----------------------------- | ------------------------------ |
| `validate_usda_load.sql`     | Verify ETL data integrity     | After ETL runs                 |
| `check_etl_summary.sql`      | Overview of data counts       | Quick health check             |
| `check_commodity_status.sql` | Commodity-specific validation | Troubleshooting specific crops |

### Debugging Scripts

| Script                          | Purpose                           | When to Use                               |
| ------------------------------- | --------------------------------- | ----------------------------------------- |
| `debug_missing_commodities.sql` | Find missing/filtered commodities | When ETL records don't match expectations |
| `view_commodity_mappings.sql`   | Inspect commodity mappings        | Verify mapping configuration              |
| `all_checks.sql`                | Comprehensive diagnostics         | Full system health check                  |

### Setup/Reset Scripts

| Script                           | Purpose                   | When to Use             |
| -------------------------------- | ------------------------- | ----------------------- |
| `bootstrap_usda_commodities.sql` | Initialize commodity data | Fresh database setup    |
| `reset_usda_data.sql`            | Clear USDA tables         | Clean slate for testing |

## Example Workflow

```bash
# 1. Start services
pixi run start-services

# 2. Check configured port and connect
POSTGRES_PORT=$(grep POSTGRES_PORT resources/docker/.env | cut -d'=' -f2)
psql -h localhost -p $POSTGRES_PORT -U biocirv_user -d biocirv_db -c "SELECT version();"

# 3. Run diagnostics
psql -h localhost -p $POSTGRES_PORT -U biocirv_user -d biocirv_db -f src/ca_biositing/pipeline/tests/USDA/all_checks.sql

# 4. If issues found, investigate specific area
psql -h localhost -p $POSTGRES_PORT -U biocirv_user -d biocirv_db -f src/ca_biositing/pipeline/tests/USDA/debug_missing_commodities.sql

# 5. Run Python diagnostics for more detail
pixi run python src/ca_biositing/pipeline/tests/USDA/test_api_names.py
```

## Environment Variables

The Python scripts automatically load environment variables from the project
root `.env` file:

```bash
# Required in .env file:
USDA_NASS_API_KEY=your_api_key_here
DATABASE_URL=postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:${POSTGRES_PORT}/biocirv_db
```

## Tips

- **Run `pixi run service-status` first** to ensure database is running
- **Check `resources/docker/.env` for `POSTGRES_PORT`** to find your configured
  port
- **Check logs** with `pixi run service-logs` if connections fail
- **All Python scripts have port fallback** (configured → 5432) built-in
- **SQL scripts work with any PostgreSQL client** once connected
