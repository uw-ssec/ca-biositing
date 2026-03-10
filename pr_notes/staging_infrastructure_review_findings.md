# PR Review: Staging Infrastructure (`chore/staging-tests`)

This document tracks findings, testing results, and documentation gaps
discovered during the review of the staging deployment infrastructure.

## Review Overview

- **Branch:** `chore/staging-tests`
- **Focus:** GCP Deployment via Pulumi (Cloud Run, Cloud SQL, Secret Manager)
- **Reviewer:** Roo

## Findings

### Infrastructure Setup

- [x] Switch to branch and pull upstream changes.
- [x] Read and understand `deployment/README.md`.
- [x] Identify core services: FastAPI Webservice, Prefect Server, Prefect
      Worker, Cloud SQL (PostgreSQL 17), and Secret Manager.
- [x] Review Pulumi Python structure (`deploy.py`, `cloud_run.py`, etc.).

### Testing Database Connectivity

- [x] Retrieve read-only database password from Secret Manager.
- [x] Establish tunnel via Cloud SQL Auth Proxy (using v1 syntax).
- [x] Connect and query database as `biocirv_readonly` via `psql`.

## Documentation Gaps & Suggestions

### Gap 1: Local Credential Requirements for Pulumi Tasks

**Issue:** The `pixi` tasks that run Pulumi inside Docker containers (e.g.,
`cloud-outputs`, `cloud-plan`) expect Google Cloud Application Default
Credentials (ADC) to be present at
`~/.config/gcloud/application_default_credentials.json`. **Finding:** Running
`gcloud auth login` is insufficient; `gcloud auth application-default login` is
also required. **Suggested Addition:** Add the ADC login step to the "Sign into
gcloud CLI" section of `deployment/README.md`.

### Gap 2: Pulumi Local Image Build Requirement

**Issue:** The `cloud-outputs` and `cloud-deploy` tasks fail if the
`ca-biositing-pulumi` Docker image has not been built locally. **Finding:**
There is no explicit instruction in the "First-Time Setup" to run
`pixi run -e deployment cloud-build`. **Suggested Addition:** Add
`pixi run -e deployment cloud-build` as the very first step in "First-Time
Setup" in `deployment/README.md`.

### Gap 3: Missing `pixi run` for Cloud SQL Proxy

**Issue:** The `deployment/README.md` suggests running `cloud-sql-proxy`
directly. **Finding:** The binary is only available within the Pixi `deployment`
environment. **Suggested Addition:** Update documentation to use
`pixi run -e deployment cloud-sql-proxy ...`.

### Gap 4: Missing Cloud SQL Proxy Dependency

**Issue:** README claims the proxy is available in the Pixi environment, but it
is not listed in `pixi.toml`. **Finding:** Users must manually install it via
`gcloud components install`. **Suggested Addition:** Add
`google-cloud-sql-proxy` to `pixi.toml` dependencies or provide an
`install-proxy` task.

### Gap 5: GCloud Component Python Conflict

**Issue:** Installing components via `gcloud` (like the proxy) triggers a prompt
to install Python 3.13. **Finding:** This conflicts with the Pixi-managed Python
3.12 environment and requires a manual "no" to proceed. **Suggested Addition:**
Note in documentation to decline Python 3.13 during component installation.

### Gap 6: Cloud SQL Proxy v1 vs v2 Syntax

**Issue:** The README uses v2 syntax (`--port`), but the `gcloud` component
often installs v1 (`-instances`). **Finding:** v1 requires
`-instances=CONNECTION_NAME=tcp:PORT` while v2 uses
`CONNECTION_NAME --port PORT`. **Suggested Addition:** Document both syntaxes or
pin the proxy version.

### Gap 7: `psql` availability

**Issue:** The README implies `psql` is available globally for testing.
**Finding:** Like the proxy, `psql` is a dependency within the Pixi `deployment`
environment. **Suggested Addition:** Update documentation to use
`pixi run -e deployment psql ...`.

### Gap 8: Refreshing Views on Staging

**Issue:** Documentation for `refresh-views` only covers local Docker usage.
**Finding:** To refresh views on staging, users must override `DATABASE_URL` to
point through the proxy. Furthermore, the `pixi.toml` task has a hardcoded `env`
block that prevents overrides, requiring the Python command to be run directly.
**Suggested Addition:** Update `pixi.toml` to use a default `DATABASE_URL` only
if not provided, or document the direct Python command for staging.

## Significant Findings

- **Containerized Pulumi:** The use of Docker for Pulumi execution is a robust
  solution for avoiding the known gRPC fork/crash issues on macOS, but it
  introduces a dependency on the local Docker daemon and specific volume mounts
  for credentials.
- **Tracking:** The local branch was successfully configured to track
  `upstream/chore/staging-tests`.
- **GCS Buckets:** The infrastructure **does not** currently manage
  application-level storage buckets. Only the Pulumi state bucket
  (`biocirv-470318-pulumi-state`) is in use.
- **Postgres Extensions:** Verified that `postgis` (v3.6.0) is correctly enabled
  on the staging instance.
- **Materialized Views:** Noted a significant number of `NULL` values introduced
  in the `analysis_average_view` materialized view. This may impact downstream
  analytics and should be investigated to determine if it is a result of the new
  ETL logic or underlying data gaps.

### Gap 9: Missing `PREFECT_WORK_POOL_NAME` in local `.env`

**Issue:** The `prefect.yaml` was updated to use `{{ $PREFECT_WORK_POOL_NAME }}`
for environment-agnostic deployments, but this variable is missing from existing
local `.env` files. **Finding:** Running `pixi run deploy` fails with a cryptic
error about the work pool name literal `{{ $PREFECT_WORK_POOL_NAME }}` not
existing because the template is not resolved. **Suggested Addition:** Update
the "Local Development" or "First-Time Setup" section to ensure users add
`PREFECT_WORK_POOL_NAME=biocirv_dev_work_pool` to their `.env`.
