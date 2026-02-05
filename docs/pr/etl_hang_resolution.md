# PR Summary: Resolving ETL Pipeline Hangs and Deadlocks

## Overview

This PR addresses a critical issue where the Prefect ETL pipeline would hang
indefinitely during various stages of execution (Import, Transformation, and
Loading). The root causes were identified as module-level import deadlocks and
incorrect database connectivity handling within the Dockerized environment.

## Findings & Root Causes

### 1. Module-Level Import Deadlocks

**Issue**: Transformation and Loading modules were importing the entire
SQLAlchemy data model (`from ...generated.ca_biositing import *`) and Pydantic
settings at the top level. **Cause**: In a process-based Prefect worker on
macOS/Docker, simultaneous module-level imports of heavy dependencies can
trigger a deadlock in the Python interpreter's global import lock. The worker
would stall before even entering the task logic.

### 2. Database Connectivity in Docker

**Issue**: The database engine was often hardcoded or defaulted to `localhost`.
**Cause**: Inside a Docker container, the database is reachable via the `db`
hostname, not `localhost`. Attempts to connect to `localhost` from within the
container resulted in hangs or timeouts.

### 3. Blocking I/O at Import Time

**Issue**: The `engine.py` and `database.py` modules were performing
connectivity tests (`engine.connect()`) immediately upon being imported.
**Cause**: Performing network I/O during a module import is a dangerous
anti-pattern that frequently leads to deadlocks in orchestrated environments
like Prefect.

## Relevant Changes

### Lazy Loading Architecture

- **Flows**: Moved all ETL component imports (Extract, Transform, Load) inside
  the flow functions.
- **Tasks**: Moved SQLAlchemy model imports and `settings` access inside the
  `@task` functions.
- **Utilities**: Refactored `name_id_swap.py` to import the database engine
  lazily.

### Robust Database Handling

- **Unified Engine**: Refactored `datamodels/database.py` to be the single,
  Docker-aware source of truth for the database engine.
- **Direct Engine Creation**: Updated loaders to create isolated engines with
  optimized pool settings (`pool_size=5`, `max_overflow=0`) to prevent resource
  contention.
- **Explicit Handshake**: Added explicit `engine.connect()` blocks to provide
  clear debug visibility and ensure the network path is open before starting
  sessions.

### Orchestration Optimization

- **Sub-flow Invocation**: Updated `run_prefect_flow.py` to use `.fn()` for
  sub-flows, bypassing unnecessary orchestration overhead in local development.

## Best Practices Moving Forward

1.  **Never Import Heavy Models at Top Level**: Always import SQLAlchemy models
    and Pydantic settings inside the function/task where they are used.
2.  **Avoid Import-Time I/O**: Modules should never attempt to connect to a
    database or file system during the `import` phase.
3.  **Use Docker-Aware Hostnames**: Always check for the existence of
    `/.dockerenv` to determine if the code should connect to `db` or
    `localhost`.
4.  **Local vs. Production Orchestration**:
    - **Local/Docker**: Use `sub_flow.fn()` when calling flows from within a
      master flow to avoid scheduling deadlocks in single-worker environments.
    - **Production (GCP/Cloud Run)**: Use standard sub-flow calls or
      `run_deployment` to allow Prefect to track individual runs and manage
      infrastructure scaling.
5.  **Granular Debug Logging**: Use `print()` statements alongside `logger` for
    critical lifecycle events (Session open, Commit, Batch start) to identify
    hangs that occur outside the logger's context.
