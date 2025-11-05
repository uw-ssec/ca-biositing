# Pipeline Tests

This directory contains minimal tests for the `ca_biositing.pipeline` namespace
package.

## Running Tests

To run all tests for the pipeline package:

```bash
pixi run pytest src/ca_biositing/pipeline -v
```

## Test Structure

### `conftest.py`

Contains shared pytest fixtures:

- `engine`: Creates an in-memory SQLite database for testing
- `session`: Provides a database session for tests that need persistence

### `test_package.py`

Tests for package metadata:

- Verifies package version
- Tests package imports

### `test_lookup_utils.py`

Tests for utility functions in `utils/lookup_utils.py`:

- `test_replace_id_with_name_df`: Tests replacing ID columns with names
- `test_replace_name_with_id_df_existing_names`: Tests replacing names with
  existing IDs
- `test_replace_name_with_id_df_new_names`: Tests creating new entries when
  names don't exist
- `test_replace_name_with_id_df_preserves_other_columns`: Tests that other
  DataFrame columns are preserved

### `test_etl_extract.py`

Tests for ETL extract functions:

- `test_extract_basic_sample_info_import`: Tests function import
- `test_extract_basic_sample_info_success`: Tests successful data extraction
  (mocked)
- `test_extract_basic_sample_info_failure`: Tests failure handling

### `test_flows.py`

Tests for Prefect flows:

- `test_primary_product_flow_import`: Tests primary product flow import
- `test_analysis_type_flow_import`: Tests analysis type flow import

## Test Coverage

The tests cover:

- ✅ Package metadata and imports
- ✅ Lookup utility functions (ID ↔ name mappings)
- ✅ ETL extract function imports and basic behavior
- ✅ Prefect flow imports and callability

## Adding New Tests

When adding new pipeline functionality:

1. Create a new test file following the naming pattern `test_<module_name>.py`
2. Import the modules/functions to test
3. Write tests for critical functionality
4. Use mocking for external dependencies (Google Sheets, databases, etc.)
5. Run tests to verify they pass

Example test for a new utility function:

```python
def test_my_new_function():
    """Test my new utility function."""
    from ca_biositing.pipeline.utils.my_module import my_function

    result = my_function("test input")
    assert result == "expected output"
```

Example test with database session:

```python
def test_my_function_with_db(session):
    """Test function that uses database."""
    from ca_biositing.datamodels.biomass import Biomass

    # Create test data
    biomass = Biomass(biomass_name="Test")
    session.add(biomass)
    session.commit()

    # Test your function
    # ...
```

## Mocking External Dependencies

For functions that interact with external services (Google Sheets, APIs, etc.),
use mocking:

```python
from unittest.mock import patch

@patch("ca_biositing.pipeline.utils.gsheet_to_pandas.gsheet_to_df")
def test_extract_function(mock_gsheet):
    """Test extraction with mocked Google Sheets."""
    mock_gsheet.return_value = pd.DataFrame({"col": ["val"]})

    # Test your function
    # ...
```

## Notes

- **Prefect Tasks**: Access the underlying function with `.fn` attribute for
  testing without Prefect runtime
- **Database Tests**: Use the `session` fixture for tests requiring database
  operations
- **External Services**: Always mock external API calls to avoid network
  dependencies
- **Coverage**: Focus on critical business logic and utility functions
