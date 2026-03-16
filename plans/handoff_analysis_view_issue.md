# Handoff: Investigation of `analysis_average` View Population Issues

## Context

The project has recently undergone a significant architectural shift to
standardize on **lowercase naming** for geographic and resource-related data to
ensure integrity across multiple ETL pipelines (`usda`, `field_sample`,
`landiq`, etc.).

## Relevant Changes

1.  **Casing Standardization**:
    - The `place` table is now seeded with lowercase `state_name` and
      `county_name` via Alembic migration `a085cd4a462e` and
      `seed_target_counties.sql`.
    - The `name_id_swap` utility (`replace_name_with_id_df`) has been hardened
      to perform **case-insensitive lookups** and **enforce lowercase** when
      creating new "stub" records for resources and products.
    - Load tasks for `Resource` and `PrimaryAgProduct` have been updated to use
      case-insensitive matching during their check-and-update phases.

2.  **Architectural Alignment**:
    - The `field_sample` ETL now correctly bridges samples to the
      `LocationAddress` table using these standardized names.
    - `LocationAddress` lookups now normalize `address_line1` and `city` to
      lowercase.

## Preemptive Advice for View Debugging

The issue where the `analysis_average` view (or `analysis_data_view`) is not
populating correctly is highly likely related to these casing changes.

- **String Matching in Views**: Check if the view definitions (likely in
  `src/ca_biositing/datamodels/ca_biositing/datamodels/views.py`) use hardcoded
  uppercase strings or case-sensitive joins that now fail because the underlying
  data is lowercase.
- **Materialized View Refresh**: After running ETLs with the new logic, ensure
  `pixi run refresh-views` is executed. If the view is failing to populate even
  after a refresh, the join logic itself is the culprit.
- **Existing Mixed Data**: If the database was not fully wiped, there may still
  be legacy uppercase records. The `name_id_swap` utility now handles this
  during ETL, but the views might be joining on `name` columns rather than `id`
  columns, or filtering on specific casing.

## Reference Files

- [`src/ca_biositing/datamodels/ca_biositing/datamodels/views.py`](src/ca_biositing/datamodels/ca_biositing/datamodels/views.py):
  View definitions.
- [`src/ca_biositing/pipeline/ca_biositing/pipeline/utils/name_id_swap.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/utils/name_id_swap.py):
  The logic ensuring lowercase stubs.
- [`alembic/versions/a085cd4a462e_usda_etl_model_updates.py`](alembic/versions/a085cd4a462e_usda_etl_model_updates.py):
  The migration seeding lowercase places.
