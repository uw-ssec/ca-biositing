# Quick Start: Using the Geospatial Module

## Installation/Setup

The geospatial module is already integrated into the `cleaning_functions`
package. No additional installation needed.

```bash
# Just ensure the environment is set up
pixi install
```

## Import

```python
from src.ca_biositing.pipeline.ca_biositing.pipeline.utils.cleaning_functions import (
    standardize_latlon,
    detect_latlon_columns,
    split_combined_latlon,
)
```

## Three Common Scenarios

### 1. Mixed Naming Conventions in Same DataFrame

**Problem:** You have `sampling_lat`/`sampling_lon` AND `prod_latlong` in the
same dataframe.

```python
# Before: Mixed naming and formats
df = pd.DataFrame({
    'sampling_lat': [40.7, 34.0],
    'sampling_lon': [-74.0, -118.2],
    'prod_latlong': ['40.5,-74.1', '34.1,-118.3'],
})

# Solution: One-line auto-detection
df_clean = standardize_latlon(df, auto_detect=True)

# After: Standardized columns
# df_clean has: desc_lat, desc_lon (float64)
```

### 2. Only Combined Columns

**Problem:** All your location data is in a single column like `location` or
`coordinates`.

```python
# Before: Combined column
df = pd.DataFrame({
    'location': ['40.7128, -74.0060', '34.0522, -118.2437'],
})

# Solution: Auto-detect and split
df_clean = standardize_latlon(df, auto_detect=True)

# After: Separated columns
# df_clean has: desc_lat, desc_lon (float64)
```

### 3. Only Separate Columns with Various Delimiters

**Problem:** You have `latitude`/`longitude` or `lat`/`lon` with different
delimiters in some rows.

```python
# Before: Multiple delimiter formats
df = pd.DataFrame({
    'latitude': [40.7128, 34.0522],
    'longitude': [-74.0060, -118.2437],
})

# Solution: Just standardize (auto-detects types)
df_clean = standardize_latlon(df, auto_detect=True)

# After: Standard float64 format
# df_clean has: desc_lat, desc_lon (both float64)
```

## Advanced: What's Being Detected?

See all detected columns:

```python
detected = detect_latlon_columns(df)
print(f"Latitude columns: {detected['latitude']}")
print(f"Longitude columns: {detected['longitude']}")
print(f"Combined columns: {detected['combined']}")
```

## Detailed Examples

See the full reference notebook:

- **Location:**
  `src/ca_biositing/pipeline/docs/tutorials/geospatial_cleaning.ipynb`
- **Content:** Comprehensive examples with sample data, error handling, all
  naming patterns

## Functions Reference

| Function                              | Purpose                                         | Use When                                 |
| ------------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| `detect_latlon_columns(df)`           | Find all lat/lon columns by pattern             | You want to see what's detected          |
| `split_combined_latlon(df, col, ...)` | Split one column into two                       | You have `location` or `latlong` columns |
| `standardize_latlon(df, ...)`         | Full workflow: detect → split → rename → coerce | You want one-line standardization        |

## Common Parameters

All functions use these parameters:

- `auto_detect=True` — Automatically find lat/lon columns (set `False` for
  explicit control)
- `output_lat='desc_lat'` — Name for standardized latitude column
- `output_lon='desc_lon'` — Name for standardized longitude column
- `coerce_to_float=True` — Convert to float64 (invalid values → NaN)
- `sep=None` — Delimiter for split (auto-detects if None)

## Data Quality

The module handles these gracefully:

- ✓ Missing values (NaN) → preserved as NaN
- ✓ Invalid formats → NaN (logged as warning)
- ✓ Non-numeric strings → NaN (logged as warning)
- ✓ Mixed delimiters → auto-detected
- ✓ Type coercion → string to float64

## In ETL Workflows

### Prefect Task Example

```python
from prefect import task
from src.ca_biositing.pipeline.ca_biositing.pipeline.utils.cleaning_functions import standardize_latlon

@task
def standardize_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Task to standardize latitude/longitude columns."""
    return standardize_latlon(df, auto_detect=True)
```

### In Your Flow

```python
@flow
def my_etl():
    df = extract_from_sheets()
    df = clean_names_df(df)
    df = standardize_coordinates(df)  # <- Your geospatial cleaning
    load_to_db(df)
```

## Validation (Future)

Currently, the module does NOT validate coordinate ranges. That will come in a
future update:

```python
# This will be added later:
df_valid = validate_latlon(df, lat_range=(-90, 90), lon_range=(-180, 180))
```

For now, always validate manually if needed:

```python
# Manual validation
assert (df_clean['desc_lat'].between(-90, 90)).all() or df_clean['desc_lat'].isnull().any()
assert (df_clean['desc_lon'].between(-180, 180)).all() or df_clean['desc_lon'].isnull().any()
```

## Troubleshooting

**Q: Function says "No columns detected"**

- Check column names match the patterns (case-insensitive, but must contain
  `lat`/`lon`)
- Use `detect_latlon_columns(df)` to see what's being found

**Q: Coordinates are NaN after standardization**

- Check format is recognized (comma, space, semicolon, pipe, tab delimiters)
- Look at logs for parsing warnings
- Manually inspect a few rows to verify format

**Q: Need validation of ranges**

- See "Validation" section above — manual validation available now
- Full validation support coming in future update

**Q: Need more help?**

- See reference notebook: `geospatial_cleaning.ipynb`
- See integration examples: `etl_notebook.ipynb`
- Check module docstrings: `geospatial.py`

## Next Steps

1. Try it with your data:

   ```python
   df = pd.read_csv('your_data.csv')
   df_clean = standardize_latlon(df, auto_detect=True)
   ```

2. Check the reference notebook for more examples

3. Integrate into your ETL flows as shown above

4. Let us know if you need validation, geocoding, or other enhancements!
