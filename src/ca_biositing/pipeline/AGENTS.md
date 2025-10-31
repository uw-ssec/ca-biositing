# AGENTS.md - CA Biositing Pipeline

This file provides guidance to AI assistants when working with the
`ca-biositing-pipeline` namespace package.

## Package Overview

This is the **ca-biositing-pipeline** package, a PEP 420 namespace package
containing ETL (Extract, Transform, Load) pipelines and workflows for the CA
Biositing project. It depends on the shared `ca-biositing-datamodels` package
and uses Prefect for workflow orchestration.

**Package Stats:**

- **Type:** Python namespace package (PEP 420)
- **Package Name:** `ca-biositing-pipeline`
- **Import Name:** `ca_biositing.pipeline`
- **Version:** 0.1.0
- **Python:** >= 3.12
- **Build System:** Hatchling
- **License:** BSD License
- **Domain:** ETL pipelines, data workflows, Prefect orchestration, Google
  Sheets integration

## Key Concepts

### Namespace Package Structure

This package follows **PEP 420** implicit namespace package conventions:

```text
src/ca_biositing/pipeline/
├── ca_biositing/              # No __init__.py at this level (namespace)
│   └── pipeline/              # Package implementation
│       ├── __init__.py        # Package initialization
│       └── */                 # Module directories
├── tests/                     # Test suite
├── docs/                      # Workflow documentation
├── pyproject.toml            # Package metadata
└── README.md                 # Documentation
```

**CRITICAL:** The `ca_biositing/` directory does **NOT** have an `__init__.py`
file. This allows multiple packages to share the `ca_biositing` namespace.

### ETL Architecture

The pipeline follows a modular ETL pattern:

- **Extract**: Prefect tasks that pull data from sources (Google Sheets, APIs,
  files)
- **Transform**: Prefect tasks that clean, validate, and reshape data using
  pandas
- **Load**: Prefect tasks that insert data into PostgreSQL using SQLModel
- **Flows**: Prefect flows that orchestrate Extract → Transform → Load sequences

### Prefect Orchestration

All workflows use **Prefect** for:

- Task dependencies and execution order
- Logging and monitoring
- Error handling and retries
- Workflow visualization

## Dependencies & Environment

### Core Dependencies

From `pyproject.toml`:

- **ca-biositing-datamodels** (>=0.1.0): Shared database models
- **pandas** (>=2.2.0, <3): Data manipulation
- **Prefect**: Workflow orchestration
- **gspread** & **gspread-dataframe**: Google Sheets integration
- **pyjanitor**: Data cleaning utilities
- **google-auth-oauthlib**: Google authentication
- **python-dotenv** (>=1.0.1, <2): Environment variables

### Development Environment

This package is typically developed as part of the main ca-biositing project
using Pixi. See the main project's `AGENTS.md` for Pixi setup.

**For testing this package:**

```bash
# From the main project root
pixi run pytest src/ca_biositing/pipeline -v
```

**For standalone development:**

```bash
# From this directory
pip install -e .
pytest -v
```

## File Structure & Modules

### ETL Modules

Located in `ca_biositing/pipeline/etl/`:

1. **`extract/`** - Data extraction tasks
   - `basic_sample_info.py`: Extract from '01-BasicSampleInfo' worksheet
   - `experiments.py`: Extract experiment data
   - Pattern: Prefect `@task` decorated functions that return DataFrames

2. **`transform/`** - Data transformation tasks
   - `products/primary_product.py`: Transform primary product data
   - Pattern: Prefect `@task` functions that accept and return DataFrames

3. **`load/`** - Data loading tasks
   - `products/primary_product.py`: Load primary products to database
   - `analysis/`: Analysis-related load functions
   - Pattern: Prefect `@task` functions that insert data via SQLModel session

4. **`templates/`** - Template files for new ETL modules
   - `extract_template.py`: Template for extract tasks
   - `transform_template.py`: Template for transform tasks
   - `load_template.py`: Template for load tasks

### Prefect Flows

Located in `ca_biositing/pipeline/flows/`:

- **`primary_product.py`**: Primary product ETL flow
- **`analysis_type.py`**: Analysis type ETL flow
- Pattern: Prefect `@flow` decorated functions that orchestrate tasks

### Utility Modules

Located in `ca_biositing/pipeline/utils/`:

1. **`lookup_utils.py`** - Foreign key relationship helpers
   - `replace_id_with_name_df()`: Map IDs to human-readable names
   - `replace_name_with_id_df()`: Map names to IDs (get or create)

2. **`gsheet_to_pandas.py`** - Google Sheets to DataFrame conversion
   - `gsheet_to_df()`: Main extraction function

3. **`run_pipeline.py`** - Master pipeline orchestrator
   - Runs all ETL flows in sequence

4. **`clear_alembic.py`** - Database migration cleanup utility

### Documentation

Located in `docs/`:

- **`DOCKER_WORKFLOW.md`**: Docker container management
- **`ALEMBIC_WORKFLOW.md`**: Database migration workflows
- **`ETL_WORKFLOW.md`**: ETL development guide
- **`PREFECT_WORKFLOW.md`**: Prefect orchestration guide
- **`GCP_SETUP.md`**: Google Cloud setup for Sheets API

## Working with ETL Pipelines

### Extract Task Pattern

```python
from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
from ca_biositing.pipeline.utils.gsheet_to_pandas import gsheet_to_df

@task
def extract_my_data() -> Optional[pd.DataFrame]:
    """
    Extracts data from a Google Sheet.

    Returns:
        DataFrame with raw data, or None if extraction fails.
    """
    logger = get_run_logger()
    logger.info("Extracting data from worksheet...")

    GSHEET_NAME = "Your Google Sheet Name"
    WORKSHEET_NAME = "Your Worksheet Name"
    CREDENTIALS_PATH = "credentials.json"

    raw_df = gsheet_to_df(GSHEET_NAME, WORKSHEET_NAME, CREDENTIALS_PATH)

    if raw_df is None:
        logger.error("Failed to extract data.")
        return None

    logger.info(f"Extracted {len(raw_df)} rows.")
    return raw_df
```

### Transform Task Pattern

```python
from typing import Dict, Optional
import pandas as pd
from prefect import task, get_run_logger

@task
def transform_my_data(data_sources: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
    """
    Transforms raw data into the target format.

    Args:
        data_sources: Dictionary of DataFrames from extract tasks

    Returns:
        Transformed DataFrame ready for loading
    """
    logger = get_run_logger()
    logger.info("Transforming data...")

    # Get source DataFrame
    source_df = data_sources.get("source_name")
    if source_df is None or source_df.empty:
        logger.warning("No data to transform.")
        return None

    # Transform: select columns, clean, deduplicate, etc.
    transformed_df = (
        source_df
        .filter_on("column_name != ''")
        .select_columns(["col1", "col2"])
        .rename_column("col1", "new_name")
        .drop_duplicates()
    )

    logger.info(f"Transformed to {len(transformed_df)} rows.")
    return transformed_df
```

### Load Task Pattern

```python
from typing import Optional
import pandas as pd
from prefect import task, get_run_logger
from sqlmodel import Session
from ca_biositing.datamodels.your_model import YourModel
from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df

@task
def load_my_data(df: Optional[pd.DataFrame]) -> None:
    """
    Loads transformed data into the database.

    Args:
        df: Transformed DataFrame to load
    """
    logger = get_run_logger()

    if df is None or df.empty:
        logger.warning("No data to load.")
        return

    logger.info(f"Loading {len(df)} rows...")

    # Get database session
    from ca_biositing.datamodels.database import get_engine
    engine = get_engine()

    with Session(engine) as session:
        # Convert names to IDs if needed
        df = replace_name_with_id_df(
            db=session,
            df=df,
            ref_model=LookupModel,
            name_column_name="name_col",
            id_column_name="id_col"
        )

        # Insert records
        for _, row in df.iterrows():
            record = YourModel(**row.to_dict())
            session.add(record)

        session.commit()
        logger.info("Data loaded successfully.")
```

### Prefect Flow Pattern

```python
from prefect import flow
from ca_biositing.pipeline.etl.extract.my_extract import extract_my_data
from ca_biositing.pipeline.etl.transform.my_transform import transform_my_data
from ca_biositing.pipeline.etl.load.my_load import load_my_data

@flow(name="My ETL Flow", log_prints=True)
def my_etl_flow():
    """
    ETL flow for my data pipeline.

    Extracts data from source, transforms it, and loads into database.
    """
    print("Starting My ETL flow...")

    # Extract
    raw_df = extract_my_data()

    # Transform
    transformed_df = transform_my_data({"my_data": raw_df})

    # Load
    load_my_data(transformed_df)

    print("My ETL flow completed.")

# Run the flow
if __name__ == "__main__":
    my_etl_flow()
```

## Testing

### Test Structure

Tests are in the `tests/` directory:

- **`conftest.py`**: Shared fixtures (engine, session)
- **`test_package.py`**: Package metadata tests
- **`test_lookup_utils.py`**: Utility function tests
- **`test_etl_extract.py`**: Extract task tests (with mocking)
- **`test_flows.py`**: Flow import tests
- **`README.md`**: Test documentation

### Running Tests

```bash
# Run all tests (from main project root)
pixi run pytest src/ca_biositing/pipeline -v

# Run specific test file
pixi run pytest src/ca_biositing/pipeline/tests/test_lookup_utils.py -v

# Run with coverage
pixi run pytest src/ca_biositing/pipeline --cov=ca_biositing.pipeline --cov-report=html
```

### Test Fixtures

From `conftest.py`:

```python
# Use these fixtures in tests
def test_my_function(session):
    """Test using database session."""
    # session is an in-memory SQLite database
    # ...
```

Available fixtures:

- `engine`: SQLite in-memory database engine
- `session`: SQLModel session for database operations

### Testing Prefect Tasks

**Important:** Prefect tasks require special handling in tests due to logging
context.

```python
from unittest.mock import patch

@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.get_run_logger")
@patch("ca_biositing.pipeline.etl.extract.basic_sample_info.gsheet_to_df")
def test_extract_task(mock_gsheet, mock_logger):
    """Test extract task with mocked dependencies."""
    from ca_biositing.pipeline.etl.extract.basic_sample_info import extract_basic_sample_info

    # Mock logger to avoid Prefect context issues
    mock_logger.return_value.info = lambda msg: None
    mock_logger.return_value.error = lambda msg: None

    # Mock data source
    mock_gsheet.return_value = pd.DataFrame({"col": ["val"]})

    # Call the task function directly (not as Prefect task)
    result = extract_basic_sample_info.fn()

    # Verify results
    assert result is not None
    assert len(result) == 1
```

**Key points:**

- Use `.fn()` to call the underlying function without Prefect runtime
- Mock `get_run_logger()` to avoid context errors
- Mock external dependencies (Google Sheets, APIs, etc.)

### Writing Tests

**Utility Function Test:**

```python
def test_lookup_utility(session):
    """Test lookup utility function."""
    from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df
    from ca_biositing.datamodels.biomass import BiomassType

    # Create test data
    biomass_type = BiomassType(biomass_type="Test Type")
    session.add(biomass_type)
    session.commit()

    # Test the function
    df = pd.DataFrame({"biomass_type": ["Test Type"]})
    result = replace_name_with_id_df(
        db=session,
        df=df,
        ref_model=BiomassType,
        name_column_name="biomass_type",
        id_column_name="biomass_type_id"
    )

    assert "biomass_type_id" in result.columns
    assert result.loc[0, "biomass_type_id"] == biomass_type.biomass_type_id
```

## Common Tasks

### Adding a New ETL Pipeline

1. **Create extract task** in `etl/extract/my_extract.py`:
   - Use `@task` decorator
   - Return `Optional[pd.DataFrame]`
   - Use `get_run_logger()` for logging

2. **Create transform task** in `etl/transform/my_transform.py`:
   - Use `@task` decorator
   - Accept `Dict[str, pd.DataFrame]`
   - Return transformed DataFrame

3. **Create load task** in `etl/load/my_load.py`:
   - Use `@task` decorator
   - Accept DataFrame
   - Use database session to insert data

4. **Create flow** in `flows/my_flow.py`:
   - Use `@flow` decorator
   - Orchestrate extract → transform → load
   - Add to master orchestrator in `utils/run_pipeline.py`

5. **Write tests** in `tests/test_my_pipeline.py`:
   - Mock external dependencies
   - Test each task function
   - Test flow import

6. **Run and verify:**
   ```bash
   pixi run pytest src/ca_biositing/pipeline -v
   python -m ca_biositing.pipeline.flows.my_flow
   ```

### Modifying an Existing Pipeline

1. **Understand dependencies:** Check which flows use the module
2. **Update the task:** Modify extract/transform/load function
3. **Update tests:** Ensure tests cover changes
4. **Run tests:** Verify nothing breaks
5. **Test the flow:** Run the complete flow end-to-end

### Using Lookup Utilities

**Replace IDs with names (for display):**

```python
from ca_biositing.pipeline.utils.lookup_utils import replace_id_with_name_df
from ca_biositing.datamodels.biomass import BiomassType

# Convert biomass_type_id to biomass_type name
df_with_names = replace_id_with_name_df(
    db=session,
    df=df,
    ref_model=BiomassType,
    id_column_name="biomass_type_id",
    name_column_name="biomass_type"
)
```

**Replace names with IDs (for loading):**

```python
from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df
from ca_biositing.datamodels.biomass import BiomassType

# Convert biomass_type name to biomass_type_id
# Creates new entries if names don't exist
df_with_ids = replace_name_with_id_df(
    db=session,
    df=df,
    ref_model=BiomassType,
    name_column_name="biomass_type",
    id_column_name="biomass_type_id"
)
```

## Code Quality & Standards

### Pre-commit Checks

Always run pre-commit before committing:

```bash
# From main project root
pixi run pre-commit run --files src/ca_biositing/pipeline/**/*
```

### Code Style

- **Type hints:** Required for all functions
- **Docstrings:** Required for all tasks and flows
- **Prefect decorators:** Use `@task` and `@flow` appropriately
- **Logging:** Use `get_run_logger()` in Prefect tasks
- **Error handling:** Return `None` or empty DataFrame on errors (don't raise in
  tasks unless intended)

### Import Conventions

```python
# Standard library
from typing import Optional, Dict
from datetime import datetime

# Third-party
import pandas as pd
from prefect import task, flow, get_run_logger
from sqlmodel import Session

# Local - datamodels
from ca_biositing.datamodels.biomass import Biomass
from ca_biositing.datamodels.database import get_engine

# Local - pipeline
from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df
```

## Common Pitfalls & Solutions

### Issue: Import errors with namespace package

**Problem:** Can't import `ca_biositing.pipeline`

**Solution:**

- Ensure `ca_biositing/` does **NOT** have `__init__.py`
- Ensure `ca_biositing/pipeline/` **DOES** have `__init__.py`
- Install both packages: `pip install -e src/ca_biositing/datamodels` and
  `pip install -e src/ca_biositing/pipeline`
- For main project: `pixi install`

### Issue: Prefect logger context errors in tests

**Problem:** `MissingContextError: There is no active flow or task run context`

**Solution:**

- Mock `get_run_logger()` in tests
- Use `.fn()` to call task function directly without Prefect runtime
- Example:
  ```python
  @patch("module.get_run_logger")
  def test_task(mock_logger):
      mock_logger.return_value.info = lambda msg: None
      result = my_task.fn()  # Not my_task()
  ```

### Issue: Google Sheets authentication failures

**Problem:** Can't access Google Sheets

**Solution:**

- Ensure `credentials.json` exists and is valid
- Follow `docs/GCP_SETUP.md` for complete setup
- Check service account has access to the sheet
- Verify `.env` file configuration

### Issue: Database connection errors

**Problem:** Can't connect to PostgreSQL

**Solution:**

- For Docker: Ensure containers are running (`docker-compose up -d`)
- Check `.env` file has correct database credentials
- Verify database migrations are applied (`alembic upgrade head`)
- Ensure datamodels package is installed

### Issue: Pandas chaining errors

**Problem:** `SettingWithCopyWarning` or unexpected results

**Solution:**

- Always use `.copy()` when modifying DataFrames
- Use pyjanitor's method chaining for cleaner transforms
- Example:
  ```python
  df = (
      source_df.copy()
      .filter_on("col != ''")
      .select_columns(["col1", "col2"])
  )
  ```

### Issue: SQLModel deprecation warnings

**Problem:** Warning about `session.query()` vs `session.exec()`

**Solution:**

- Prefer `session.exec()` for SQLModel queries
- Current code uses `.query()` - this is a known issue
- When refactoring:

  ```python
  # Old
  records = session.query(Model).all()

  # New
  from sqlmodel import select
  records = session.exec(select(Model)).all()
  ```

## Integration with Main Project

### Usage in Prefect Workflows

Run flows from command line or Python:

```bash
# Run specific flow
python -m ca_biositing.pipeline.flows.primary_product

# Run all flows (master orchestrator)
python -m ca_biositing.pipeline.utils.run_pipeline
```

### Usage with Docker

```bash
# Build and start containers
docker-compose build
docker-compose up -d

# Run pipeline in container
docker-compose exec app python utils/run_pipeline.py

# View logs
docker-compose logs -f app
```

### Database Migrations

- Migrations are managed with Alembic
- Database models come from `ca-biositing-datamodels` package
- See `docs/ALEMBIC_WORKFLOW.md` for migration workflows
- Migration files are in `alembic/versions/`

### Shared Data Models

- Import models from `ca_biositing.datamodels`
- Don't create models in the pipeline package
- Coordinate model changes with database migrations

## Best Practices

1. **Namespace Package:** Never add `__init__.py` to `ca_biositing/` directory
2. **Prefect Tasks:** Use `@task` for ETL functions, `@flow` for orchestration
3. **Error Handling:** Return None/empty DataFrame on errors; log with
   `get_run_logger()`
4. **Type Hints:** Use `Optional[pd.DataFrame]` for nullable returns
5. **Logging:** Always use `get_run_logger()` in Prefect tasks
6. **Mocking:** Mock external dependencies (Google Sheets, logger) in tests
7. **Database Sessions:** Use `with Session(engine)` context manager
8. **Lookup Utils:** Use helper functions for foreign key relationships
9. **Templates:** Use template files in `etl/templates/` for new modules
10. **Documentation:** Keep README.md and workflow docs up to date
11. **Dependencies:** Ensure datamodels package is installed
12. **Testing:** Write tests for all new ETL tasks and utilities

## Workflow Documentation

Detailed guides are available in the `docs/` directory:

- **`DOCKER_WORKFLOW.md`**: Container management and deployment
- **`ALEMBIC_WORKFLOW.md`**: Database schema migrations
- **`ETL_WORKFLOW.md`**: ETL development and patterns
- **`PREFECT_WORKFLOW.md`**: Prefect orchestration and best practices
- **`GCP_SETUP.md`**: Google Cloud and Sheets API setup

## Version Information

- **Current Version:** 0.1.0
- **Python:** >= 3.12
- **Prefect:** Latest
- **pandas:** >= 2.2.0, < 3
- **ca-biositing-datamodels:** >= 0.1.0

## Related Documentation

- **Main Project AGENTS.md:**
  `/Users/lsetiawan/Repos/SSEC/ca-biositing/AGENTS.md`
- **Datamodels AGENTS.md:** `../datamodels/AGENTS.md`
- **Package README:** `README.md` (in this directory)
- **Test Documentation:** `tests/README.md`
- **Prefect Docs:** <https://docs.prefect.io/>
- **pandas Docs:** <https://pandas.pydata.org/docs/>
- **SQLModel Docs:** <https://sqlmodel.tiangolo.com/>

## Trust These Instructions

These instructions were generated through analysis of the package structure,
dependencies, and integration patterns. **Follow these guidelines when:**

- Adding or modifying ETL pipelines
- Writing Prefect tasks and flows
- Testing pipeline components
- Troubleshooting import or runtime issues

**Only search for additional information if:**

- Instructions appear outdated or produce errors
- Working with advanced Prefect features not covered here
- Implementing new integration patterns not documented here
- Debugging complex Google Sheets authentication issues

For routine pipeline development, testing, and maintenance, these instructions
provide complete guidance.
