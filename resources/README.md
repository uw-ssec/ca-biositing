# Resources Directory

This directory contains deployment resources and configuration files for running
the ca-biositing ETL pipeline in a containerized environment with Prefect
orchestration.

## Directory Structure

```text
resources/
├── docker/          # Docker configuration files
│   ├── .dockerignore
│   ├── .env.example         # Template for environment variables
│   ├── create_prefect_db.sql # Database initialization script
│   ├── docker-compose.yml   # Service orchestration configuration
│   └── pipeline.dockerfile  # Multi-stage build for production
└── prefect/         # Prefect workflow orchestration files
    ├── deploy.py            # Deployment automation script
    ├── prefect.yaml         # Prefect deployment configuration
    └── run_prefect_flow.py  # Master flow orchestration
```

## Overview

### Docker Resources (`docker/`)

The `docker/` directory contains all necessary files for containerizing and
running the ETL pipeline:

- **docker-compose.yml**: Orchestrates multiple services including PostgreSQL
  database, Prefect server, and Prefect worker
- **pipeline.dockerfile**: Multi-stage Dockerfile using Pixi for dependency
  management
- **create_prefect_db.sql**: Initializes the Prefect metadata database
- **.env.example**: Template for required environment variables
- **.env**: Local environment configuration (not tracked in git)

### Prefect Resources (`prefect/`)

The `prefect/` directory contains workflow orchestration configuration:

- **prefect.yaml**: Defines deployment configurations for ETL flows
- **deploy.py**: Automates the deployment process with retry logic
- **run_prefect_flow.py**: Master flow that orchestrates all ETL sub-flows

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Valid `.env` file in `resources/docker/` (copy from `.env.example`)
- Google Cloud credentials (`credentials.json`) at project root

### Starting the Environment

From the project root directory:

```bash
# Start all services (database, Prefect server, worker)
pixi run start-services

# Check service status
pixi run service-status

# View logs
pixi run service-logs
```

### Deploying Flows

```bash
# Deploy flows to Prefect server (using the pipeline deploy task)
pixi run deploy

# Or deploy with specific parameters
pixi run deploy --deployment-name master-etl-deployment
```

### Running Flows

```bash
# Trigger the master ETL flow
pixi run run-etl
```

### Monitoring

Access the Prefect UI at: [http://localhost:4200](http://localhost:4200)

### Stopping the Environment

```bash
# Stop all services
pixi run teardown-services

# Stop and remove volumes (clears all data)
pixi run teardown-services-volumes
```

## Services Architecture

The Docker Compose configuration orchestrates four main services:

1. **`db`** (PostgreSQL 13)
   - Hosts both application and Prefect metadata databases
   - Exposed on port 5432 (configurable via `.env`)
   - Persistent storage via Docker volume

2. **`setup-db`** (One-time migration)
   - Runs Alembic migrations to initialize/upgrade database schema
   - Runs once when services start
   - Depends on `db` health check

3. **`prefect-server`**
   - Prefect orchestration server
   - Web UI on port 4200
   - Stores workflow metadata in PostgreSQL

4. **`prefect-worker`**
   - Executes flow runs from the work pool
   - Connects to Prefect server via API
   - Has access to flow code and credentials

## Configuration

### Environment Variables

Key environment variables defined in `.env`:

```bash
# PostgreSQL Settings
POSTGRES_HOST=db
POSTGRES_USER=biocirv_user
POSTGRES_DB=biocirv_db
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432

# Database URLs
DATABASE_URL=postgresql+psycopg2://...
PREFECT_API_DATABASE_CONNECTION_URL=postgresql+asyncpg://...

# Prefect Settings
PREFECT_API_URL=http://localhost:4200/api
PREFECT_SERVER_API_HOST=0.0.0.0
PREFECT_UI_API_URL=http://localhost:4200/api
```

**Important Note on Prefect URLs:**
- Use `http://localhost:4200/api` when running flows from your **host machine**
  (e.g., via `pixi run run-etl`)
- Use `http://prefect-server:4200/api` or `http://0.0.0.0:4200/api` when running
  from **within containers**
- The `.env.example` file is configured for host machine access by default

### Network Configuration

All services communicate via the `prefect-network` bridge network, allowing
container-to-container communication using service names as hostnames.

## Adding New Flows

1. Create your flow in `src/ca_biositing/pipeline/flows/`
2. Import it in `resources/prefect/run_prefect_flow.py`
3. Add to `AVAILABLE_FLOWS` dictionary
4. Define deployment in `resources/prefect/prefect.yaml`
5. Deploy: `python resources/prefect/deploy.py <deployment-name>`

## Troubleshooting

### Services Won't Start

```bash
# Check logs for all services
pixi run service-logs

# Rebuild images
pixi run rebuild-services
```

### Database Connection Issues

```bash
# Verify database is healthy
pixi run check-db-health

# Access database directly (interactive psql session)
pixi run access-db
```

### Accessing and Inspecting the Database

For debugging and data inspection, you can connect to the PostgreSQL database
directly using `psql`. The database credentials are defined in
`resources/docker/.env`.

**List all tables:**

```bash
pixi run exec-db psql -U biocirv_user -d biocirv_db -c "\dt"
```

**Query specific data:**

```bash
pixi run exec-db psql -U biocirv_user -d biocirv_db -c "SELECT * FROM your_table_name LIMIT 10;"
```

**Access interactive psql session:**

```bash
pixi run access-db
```

Once in the interactive session, you can use standard PostgreSQL commands:
- `\dt` - List all tables
- `\d table_name` - Describe table structure
- `\l` - List all databases
- `\q` - Exit psql

### Prefect Worker Not Picking Up Runs

```bash
# Check worker logs
pixi run service-logs

# Restart worker if needed
pixi run restart-prefect-worker

# Verify work pool exists in Prefect UI
# Navigate to: http://localhost:4200/work-pools
```

## Related Documentation

- **Pipeline Documentation**: See `src/ca_biositing/pipeline/docs/` for detailed
  ETL workflows
- **Main README**: Project overview at `/README.md`
- **Pipeline AGENTS**: AI assistant guidance at
  `src/ca_biositing/pipeline/AGENTS.md`

## Development vs Production

**Current Configuration**: Development setup with:

- Local PostgreSQL container
- Local Prefect server
- Process-based worker pool
- Volume mounts for hot-reloading

**For Production**:

- Use managed PostgreSQL (e.g., AWS RDS, Google Cloud SQL)
- Deploy Prefect Cloud or self-hosted server
- Use cloud-native worker pools
- Remove volume mounts, bake code into images
- Implement secrets management (not `.env` files)

## License

This project follows the license specified in the main repository LICENSE file.
