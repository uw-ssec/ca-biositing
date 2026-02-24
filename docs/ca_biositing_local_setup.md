# CA-Biositing Local Setup Guide

This guide provides verified steps to **set up and test the CA-Biositing project
locally** — including the ETL pipeline, database, Prefect orchestration, and
Docker infrastructure.

---

## Cloning and Installing

### Prerequisites

- **Homebrew**
- **Pixi** (for dependency management)
- **Docker Desktop** (running)
- **Python 3.12+**

### Commands

```bash
git clone https://github.com/uw-ssec/ca-biositing.git
cd ca-biositing
pixi install
pixi shell
```

---

## Local Setup for ETL Pipeline

### Docker + Env

```bash
cp resources/docker/.env.example resources/docker/.env
pixi run start-services
```

> This command spins up the PostgreSQL, Prefect Server, and Prefect Worker
> containers.

### Environment Variables

After copying the `.env.example`, configure these additional settings:

1. **USDA NASS API key** — Required to fetch USDA data during ETL. Get a free
   API key from the
   [USDA NASS Quick Stats API](https://quickstats.nass.usda.gov/api/) and add it
   to `resources/docker/.env`:

   ```
   USDA_NASS_API_KEY=your_api_key_here
   ```

2. **Database URL for local commands** — The `DATABASE_URL` in
   `resources/docker/.env` uses `@db:5432` (the Docker service name), which
   works inside containers but not from your host machine. To run commands like
   `pixi run migrate` locally, set `DATABASE_URL` in your shell environment to
   point to `localhost`:

   ```bash
   export DATABASE_URL=postgresql+psycopg2://biocirv_user:biocirv_dev_password@localhost:5432/biocirv_db
   ```

   This environment variable takes priority over the value in
   `resources/docker/.env`.

---

## Google Sheets Credentials (REQUIRED)

- ETL pulls data from Google Sheets
- You must have a valid Google service account JSON key
- Share the target Google Sheet with the service account email

### Where to place credentials

- Place the file at repo root:

  ca-biositing/credentials.json

- This is mounted into the Prefect worker as:

  /app/credentials.json

- Do NOT commit this file (keep it in .gitignore)

---

### Deploy + Run ETL

```bash
pixi run deploy
pixi run run-etl
```

> This deploys and executes the **Master ETL Flow** in Prefect.

---

### Prefect UI

Access Prefect at:

[http://localhost:4200](http://localhost:4200)

> Verify that the ETL flow (e.g., _Master ETL Flow / towering-caribou_) is
> visible.

---

### Database Verification

Access the PostgreSQL database:

```bash
pixi run access-db
```

Once inside the PostgreSQL shell, run:

```sql
SELECT * FROM resource LIMIT 5;
```

> Tables should exist, but may be empty if Google Sheet credentials are
> unavailable.

---

### Tear Down

Stop and remove containers:

```bash
pixi run teardown-services
```

Or to remove volumes and data as well:

```bash
pixi run teardown-services-volumes
```

---

## Test API endpoints and DB connectivity

Start API webservice:

```bash
pixi run start-webservice
```

Visit localhost at [http://127.0.0.1:8000](http://127.0.0.1:8000) to validate
the API and visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to
view API docs and try APIs using Swagger.
