# Docker Development Workflow

This guide provides a quick reference for the common Docker commands and
workflows used in this project. All Docker operations are orchestrated via
**Pixi tasks**.

---

### Core Docker Workflow

This is the standard process for running the containerized ETL system and
database.

**1. Starting Your Environment:**

To start all services (`db`, `prefect-server`, and `prefect-worker`) in the
background:

```bash
pixi run start-services
```

This command will:

- Start the PostgreSQL database.
- Start the Prefect server.
- Start the Prefect worker.

**2. Checking Status and Logs:**

```bash
# Check service status
pixi run service-status

# View logs from all services
pixi run service-logs
```

**3. Stopping Your Environment:**

```bash
# Stop services
pixi run teardown-services

# Stop and remove volumes (CAUTION: deletes all data)
pixi run teardown-services-volumes
```

---

### Rebuilding Services

If you change dependencies in `pixi.toml` or modify the Dockerfiles, you must
rebuild the images.

```bash
# Rebuild images without cache
pixi run rebuild-services

# Restart services
pixi run start-services
```

---

### Database Access

```bash
# Access the application database via psql
pixi run access-db

# Access the Prefect metadata database
pixi run access-prefect-db

# Check database health
pixi run check-db-health
```

---

### Executing Commands in Containers

If you need to run a command inside a specific container:

```bash
# Execute in Prefect worker
pixi run exec-prefect-worker <command>

# Execute in Database container
pixi run exec-db <command>
```
