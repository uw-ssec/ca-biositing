# Cleaning helpers

This package contains small, well-documented helpers for cleaning and coercing
DataFrames used by the CA Biositing ETL pipeline. Intended to be imported as:

```py
from ca_biositing.pipeline.utils.cleaning_functions import standard_clean, coerce_columns
```

Notes:

- Geometry coercion uses `shapely` if available.
- For production, consider moving Prefect task decorators around these helpers.
