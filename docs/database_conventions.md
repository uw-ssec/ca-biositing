# Database Conventions

This project uses the following conventions for qualitative ETL data and related
lookup tables:

- Lookup names are stored in lowercase.
- Parameter names use lowercase words separated by spaces, not snake case.
  - Example: `resource_use_perc_low` → `resource use perc low`
- Qualitative use case values are loaded from the `use_case_name` column in the
  source sheet.
- When a source sheet provides multiple labels for the same concept, the
  canonical database value is the lowercase `use_case_name` value.
- ETL lineage fields should be populated when the model supports them:
  - `etl_run_id`
  - `lineage_group_id`

These conventions are intended to keep lookup matching stable across ETL runs
and to align source labels with database queries that compare against lowercase
names.
