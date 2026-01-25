# CA-Biositing Local Setup Guide

This guide provides verified steps to **set up and test the CA-Biositing project locally** — including the ETL pipeline, database, Prefect orchestration, and Docker infrastructure.

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

> This command spins up the PostgreSQL, Prefect Server, and Prefect Worker containers.

---

## 3. Google Sheets Credentials (REQUIRED)
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

> Verify that the ETL flow (e.g., *Master ETL Flow / towering-caribou*) is visible.

---

### Database Verification

Access the PostgreSQL database:

```bash
pixi run access-db
SELECT * FROM biomass LIMIT 5;
```

> Tables should exist, but may be empty if Google Sheet credentials are unavailable.

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
pixi pixi run start-webservice
```

Visit localhost at http://127.0.0.1:8000/ to validate API and visit http://127.0.0.1:8000/docs to view API docs & try API's using swagger.

