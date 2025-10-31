# Datamodels Tests

This directory contains minimal tests for the `ca_biositing.datamodels`
namespace package.

## Running Tests

To run all tests for the datamodels package:

```bash
pixi run pytest src/ca_biositing/datamodels -v
```

## Test Structure

### `conftest.py`

Contains shared pytest fixtures:

- `engine`: Creates an in-memory SQLite database for testing
- `session`: Provides a database session for tests that need persistence

### `test_biomass.py`

Tests for biomass-related data models:

- Model instantiation tests for all biomass models
- Database persistence tests for key models
- Validates field types and default values

### `test_geographic_locations.py`

Tests for geographic location data models:

- Model instantiation tests for location-related models
- Database persistence tests for City and State models
- Validates geographic data handling

### `test_package.py`

Tests for package metadata:

- Verifies package version
- Tests package imports

## Test Coverage

The tests cover:

- ✅ Model instantiation and attribute assignment
- ✅ Database persistence (create, save, retrieve)
- ✅ Field type validation (Decimal, datetime, etc.)
- ✅ Default value handling
- ✅ Package metadata and imports

## Adding New Tests

When adding new data models to the package:

1. Create a new test file following the naming pattern `test_<module_name>.py`
2. Import the models to test
3. Add instantiation tests for each model
4. Add at least one persistence test using the `session` fixture
5. Run tests to verify they pass

Example:

```python
def test_my_model_creation():
    """Test creating a MyModel instance."""
    model = MyModel(field1="value1")
    assert model.field1 == "value1"

def test_my_model_persistence(session):
    """Test saving and retrieving MyModel."""
    model = MyModel(field1="value1")
    session.add(model)
    session.commit()
    session.refresh(model)

    assert model.id is not None
    retrieved = session.get(MyModel, model.id)
    assert retrieved.field1 == "value1"
```
