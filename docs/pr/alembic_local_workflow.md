# PR: Transition Alembic Workflow to Local Execution

## Description

This PR refactors the database migration workflow to run Alembic commands
locally on the host machine instead of inside Docker containers. This change
resolves a critical issue where Python's import machinery would deadlock/hang
indefinitely inside Docker Desktop (macOS) when loading the large, complex
SQLAlchemy model suite.

## Changes

- **`src/ca_biositing/datamodels/utils/orchestrate_schema_update.py`**: Updated
  to invoke `alembic revision --autogenerate` locally. It now dynamically
  configures `PYTHONPATH` and `DATABASE_URL` to connect to the Docker-hosted
  PostgreSQL instance via `localhost`.
- **`pixi.toml`**: Redefined the `migrate` task to run `alembic upgrade head`
  locally. This ensures that applying migrations is fast and avoids container
  resource constraints.
- **Cleanup**: Removed the temporary troubleshooting summary file.

## Why this is better

1. **Performance**: Local imports of the generated models take ~1 second,
   compared to hanging indefinitely in Docker.
2. **Reliability**: Bypasses known filesystem performance issues with Docker
   Desktop on macOS (VirtioFS/gRPC FUSE) when scanning deep namespace packages.
3. **Developer Experience**: `pixi run update-schema` and `pixi run migrate` now
   work instantly without requiring manual container troubleshooting.

## Impact on Production

This change only affects the **local development workflow**. Production
deployments (GCP/Cloud Run) will continue to use standard Alembic commands in a
native Linux environment, which does not suffer from the macOS-specific Docker
volume hangs.

## Verification Results

- [x] `pixi run update-schema -m "test"`: Successfully generates migration files
      locally.
- [x] `pixi run migrate`: Successfully applies migrations to the Docker database
      in < 2 seconds.
