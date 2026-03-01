# Deployment Directory

This directory contains deployment resources, specifically cloud deployment
resources, for getting the ca-biositing project up and running on Google Cloud
Platform (GCP) using Pulumi (Python).

# Directory Structure

```text
deployment
├── cloud/gcp/infrastructure/    # Pulumi project files
│   ├── Pulumi.yaml              # Pulumi project configuration
│   ├── Pulumi.staging.yaml      # Staging stack configuration
│   ├── __main__.py              # Infrastructure definitions (Python)
```

## Quick Start

### Prerequisites

- Access to the BioCirV project in GCP
- `gcloud` CLI:
  https://docs.cloud.google.com/sdk/docs/install-sdk#latest-version
- Pulumi CLI (installed automatically via pixi):

  ```bash
  pixi run -e deployment install-pulumi
  ```

  Verify installation:

  ```bash
  pixi run -e deployment pulumi version
  ```

### Sign into gcloud CLI

Run both commands to authenticate fully. The first authenticates the gcloud CLI
itself; the second creates Application Default Credentials (ADC) used by Pulumi
and other tools.

```bash
# 1. Authenticate the gcloud CLI (required for gcloud commands)
gcloud auth login

# 2. Create Application Default Credentials (required for Pulumi and SDKs)
gcloud auth application-default login
```

Make sure to configure the project property correctly. You can see it with the
following command

```bash
gcloud config get project
```

And set it correctly with

```bash
gcloud config set project <PROJECT_ID>
```

### First-Time Setup

#### 0. Build the Pulumi Docker image (one-time)

All `cloud-*` pixi tasks run Pulumi inside a Docker container. Build the image
before running any other setup steps:

```bash
docker build -t ca-biositing-pulumi deployment/cloud/gcp/infrastructure/
```

This only needs to be re-run if `deployment/cloud/gcp/infrastructure/Dockerfile`
changes.

#### 1. Create the Pulumi state bucket (one-time)

This creates a GCS bucket to store Pulumi state files. Only needs to be run once
per project.

```bash
pixi run -e deployment cloud-bootstrap
```

#### 2. Login to the Pulumi backend

```bash
pixi run -e deployment cloud-init
```

#### 3. Initialize the staging stack (one-time)

```bash
cd deployment/cloud/gcp/infrastructure
pixi run -e deployment pulumi stack init staging
```

#### 4. Import existing resources (one-time)

If GCP resources already exist and need to be imported into Pulumi state:

```bash
# Import the Cloud SQL instance
pixi run -e deployment pulumi import \
  gcp:sql/databaseInstance:DatabaseInstance staging-db-instance \
  projects/biocirv-470318/instances/biocirv-staging \
  --stack staging --yes

# Import the Cloud SQL database
pixi run -e deployment pulumi import \
  gcp:sql/database:Database staging-db \
  biocirv-470318/biocirv-staging/biocirv-staging \
  --stack staging --yes
```

### Deploying Changes

From the project root directory:

```bash
# Preview pending changes
pixi run -e deployment cloud-plan

# Deploy pending changes
pixi run -e deployment cloud-deploy
```

### DANGEROUS: Destroy All GCP Resources

From the project root directory:

```bash
pixi run -e deployment cloud-destroy
```

Certain pieces of infrastructure with deletion retention policies may fail to
delete when this is run. If you really want to delete them, change that
infrastructure's configuration in `__main__.py`, deploy these changes with
`pixi run -e deployment cloud-plan` and `pixi run -e deployment cloud-deploy`,
and then retry running the above command.

## Troubleshooting

### Pulumi CLI not found

Install Pulumi into the pixi environment:

```bash
pixi run -e deployment install-pulumi
```

### Authentication errors

Make sure you are logged into gcloud (both commands are required):

```bash
gcloud auth login
gcloud auth application-default login
```

### State backend errors

If you see errors about the state backend, make sure you've run:

```bash
pixi run -e deployment cloud-init
```

### Resources already exist errors during `pulumi up`

If you run `pulumi up` before importing existing resources, Pulumi will try to
create resources that already exist in GCP. Follow the import steps in the
"First-Time Setup" section above.

## Staging Environment

### Architecture Overview

The staging environment runs on GCP with the following components:

| Component                         | Service                                                                |
| --------------------------------- | ---------------------------------------------------------------------- |
| **Webservice** (FastAPI)          | Cloud Run Service                                                      |
| **Prefect Server** (UI + API)     | Cloud Run Service                                                      |
| **Prefect Worker** (process type) | Cloud Run Service (internal, polls server, runs flows as subprocesses) |
| **Database**                      | Cloud SQL (PostgreSQL + PostGIS)                                       |
| **Secrets**                       | Secret Manager (DB password, GSheets creds, Prefect auth)              |

Infrastructure is managed by Pulumi (Python Automation API) with state stored in
GCS.

To retrieve service URLs:

```bash
gcloud run services list --region=us-west1 --format="table(name,status.url)"
```

### Deploy / Update Infrastructure

```bash
# Preview changes
pixi run -e deployment cloud-plan

# Apply changes
pixi run -e deployment cloud-deploy
```

### Build & Push Container Images

Build container images (`webservice`, `pipeline`) via Cloud Build:

```bash
pixi run -e deployment cloud-build-images
```

Verify images exist:

```bash
gcloud container images list --repository=gcr.io/$(gcloud config get project)
```

### Run Database Migrations

Build the pipeline image, refresh the Cloud Run job's image digest, and apply
Alembic migrations in one step:

```bash
pixi run cloud-migrate
```

This runs three steps in order:

1. `cloud-build-images` — builds and pushes the pipeline image to GCR via Cloud
   Build.
2. `gcloud run jobs update ... --image=...` — re-pins the Cloud Run job to the
   newly pushed image digest (required because Pulumi pins the digest at deploy
   time and does not detect `:latest` tag updates).
3. `gcloud run jobs execute biocirv-alembic-migrate --region=us-west1 --wait` —
   runs the migration job and waits for it to complete.

Verify the execution completed:

```bash
gcloud run jobs executions list --job=biocirv-alembic-migrate --region=us-west1 --limit=1
```

### Prefect Server Access

The Prefect server is currently deployed **without** HTTP Basic Auth for
staging. This is because Prefect's WebSocket events client (required by process
workers) does not send auth headers, causing the worker to crash at startup.

**Access the Prefect UI:**

```bash
# Get the Prefect server URL
gcloud run services describe biocirv-prefect-server --region=us-west1 --format="value(status.url)"
```

Open the returned URL in a browser.

**Configure Prefect CLI for staging:**

```bash
export PREFECT_API_URL=$(gcloud run services describe biocirv-prefect-server --region=us-west1 --format="value(status.url)")/api
```

### Trigger ETL Flows

With the Prefect CLI configured (see above):

```bash
# List deployments
prefect deployment ls

# Trigger a flow run
prefect deployment run "Master ETL Flow/master-etl-deployment"
```

Monitor in the Prefect UI or via the worker's Cloud Run logs:

```bash
gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=50
```

### Read-Only Database Users

The `biocirv_readonly` Cloud SQL user is created by Pulumi (password stored in
Secret Manager as `biocirv-staging-ro-biocirv_readonly`). Read-only privileges
are granted automatically by the `0002_grant_readonly_permissions` Alembic
migration, which runs as part of `pixi run cloud-migrate`.

Retrieve the read-only password from Secret Manager (requires appropriate IAM
permissions):

```bash
gcloud secrets versions access latest --secret=biocirv-staging-ro-biocirv_readonly
```

### Connecting to the Database (DBeaver / GUI Client)

Use the Cloud SQL Auth Proxy to create a local tunnel, then connect your client
to `localhost`:

#### 1. Install and start the proxy

Install the Cloud SQL Auth Proxy via gcloud or by downloading the binary:

```bash
gcloud components install cloud-sql-proxy
```

> **Note:** When prompted during `gcloud components install`, decline the Python
> 3.13 installation to avoid conflicting with the Pixi-managed Python 3.12
> environment.

Then start the proxy (leave it running in a separate terminal):

**Cloud SQL Auth Proxy v2 (installed by `gcloud components install`):**

```bash
cloud-sql-proxy biocirv-470318:us-west1:biocirv-staging --port 5434
```

**Cloud SQL Auth Proxy v1 (if you installed the older binary directly):**

```bash
cloud_sql_proxy -instances=biocirv-470318:us-west1:biocirv-staging=tcp:5434
```

Alternatively, download the binary directly from
https://cloud.google.com/sql/docs/mysql/sql-proxy.

#### 2. Get the password

```bash
# Primary user
gcloud secrets versions access latest --secret=biocirv-staging-db-password

# Read-only user
gcloud secrets versions access latest --secret=biocirv-staging-ro-biocirv_readonly
```

#### 3. Connection settings

| Field    | Value                                                |
| -------- | ---------------------------------------------------- |
| Host     | `127.0.0.1`                                          |
| Port     | `5434`                                               |
| Database | `biocirv-staging`                                    |
| Username | `biocirv_user` (or `biocirv_readonly` for read-only) |
| Password | (from step 2)                                        |
| SSL      | off (the proxy handles encryption to Cloud SQL)      |

### Staging Troubleshooting

#### Prefect worker not connecting

Check worker logs:

```bash
gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=20
```

Verify the worker can reach the Prefect server — look for connection errors.

#### Flow runs stuck in "Pending"

1. Verify the work pool (`biocirv-staging-pool`, type `process`) is online in
   the Prefect UI
2. Check the worker logs for errors:
   `gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=20`
3. Verify the worker container has `DATABASE_URL` and `PREFECT_API_URL` set

#### Credential rotation

1. Update the secret version in Secret Manager
2. Redeploy both Prefect services to pick up the new secret:
   ```bash
   pixi run -e deployment cloud-deploy
   ```

#### PostgreSQL extensions not enabled

Connect to the database and enable the extensions. Note that `psql` is **not**
bundled in the pixi environment — install it separately:

- macOS: `brew install libpq` (adds `psql` to PATH)
- Linux: `sudo apt install postgresql-client`

```bash
gcloud sql connect biocirv-staging --user=postgres --database=biocirv-staging
```

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS btree_gin;
SELECT PostGIS_Version();
SELECT extname FROM pg_extension WHERE extname IN ('pg_trgm', 'unaccent', 'btree_gin');
```

---

## Full Staging Deployment Runbook

Follow these steps in order for a complete staging deployment — from building
images through database migration, Prefect deployment registration, and ETL
execution.

### Prerequisites

- `gcloud` CLI authenticated: `gcloud auth login` and
  `gcloud auth application-default login`
- Docker daemon running (for local builds)
- `pixi` installed
- Access to the BioCirV GCP project (`biocirv-470318`)
- `credentials.json` service account file for Google Sheets/Drive access

### Step 1: Build and Push Container Images

```bash
pixi run cloud-build-images
```

This builds and pushes the `pipeline` and `webservice` images to GCR via Cloud
Build.

### Step 2: Deploy / Update Infrastructure

```bash
pixi run cloud-deploy
```

This creates or updates all GCP resources: Cloud SQL instance, Secret Manager
secrets, Cloud Run services (webservice, prefect-server, prefect-worker), and
the migration job. New resources after recent changes include:

- Secret: `biocirv-staging-usda-nass-api-key`
- Worker env vars: `USDA_NASS_API_KEY`, `CREDENTIALS_PATH`,
  `GOOGLE_APPLICATION_CREDENTIALS`, `LANDIQ_SHAPEFILE_URL`
- Volume: `gsheets-credentials` (Secret Manager volume mount at
  `/app/gsheets-credentials`)

### Step 3: Upload Secrets (post-deploy, manual)

These secrets must be populated manually after `cloud-deploy` creates the secret
shells:

```bash
# 1. GSheets / Google Drive service account credentials
gcloud secrets versions add biocirv-staging-gsheets-credentials \
  --data-file=credentials.json \
  --project=biocirv-470318

# 2. USDA NASS API key (replace with actual key value)
echo -n "YOUR_USDA_NASS_API_KEY" | \
  gcloud secrets versions add biocirv-staging-usda-nass-api-key \
  --data-file=- \
  --project=biocirv-470318
```

Verify the secret versions were created:

```bash
gcloud secrets versions list biocirv-staging-gsheets-credentials --project=biocirv-470318
gcloud secrets versions list biocirv-staging-usda-nass-api-key --project=biocirv-470318
```

### Step 4: Run Database Migrations

```bash
pixi run cloud-migrate
```

This rebuilds the pipeline image, updates the migration job's image digest, and
runs `alembic upgrade head` in Cloud Run.

Verify migration succeeded:

```bash
gcloud run jobs executions list --job=biocirv-alembic-migrate --region=us-west1 --limit=1
```

Expected: `SUCCEEDED` status.

### Step 5: Force New Cloud Run Revision for Worker

After uploading secrets, force a new revision to pick up the latest image and
mounted secret:

```bash
gcloud run services update biocirv-prefect-worker \
  --image=gcr.io/biocirv-470318/pipeline:latest \
  --region=us-west1
```

### Step 6: Set PREFECT_API_URL

```bash
export PREFECT_API_URL=$(gcloud run services describe biocirv-prefect-server \
  --region=us-west1 --format="value(status.url)")/api
```

### Step 7: Register Prefect Deployment

```bash
cd resources/prefect
python deploy.py master-etl-deployment --env-file ../docker/.env
```

Or with the Prefect CLI directly:

```bash
prefect --no-prompt deploy --name master-etl-deployment
```

Verify the deployment is registered:

```bash
prefect deployment ls
```

### Step 8: Trigger a Flow Run

```bash
prefect deployment run "Master ETL Flow/master-etl-deployment"
```

Monitor the run:

```bash
# Worker logs (flow execution output)
gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=100

# Or watch the Prefect UI
gcloud run services describe biocirv-prefect-server --region=us-west1 --format="value(status.url)"
```

### Step 9: Verify Data in Cloud SQL

Connect via Cloud SQL Auth Proxy (see "Connecting to the Database" section),
then:

```sql
-- Resource information (Google Sheets flow)
SELECT count(*) FROM resource_information;
-- Analysis records (Google Sheets flow)
SELECT count(*) FROM analysis_record;
-- USDA data (API flow)
SELECT count(*) FROM usda_census_survey;
-- LandIQ data (if LANDIQ_SHAPEFILE_URL was configured)
SELECT count(*) FROM landiq_record;
-- Billion Ton data (Google Drive flow)
SELECT count(*) FROM billion_ton;
```

Expected: Non-zero counts for flows that have valid data sources.

---

## Environment Variables Reference

All environment variables injected into the Prefect worker Cloud Run service:

| Variable                         | Source                                               | Description                                      |
| -------------------------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `PREFECT_API_URL`                | Derived from prefect-server URI                      | Prefect API endpoint                             |
| `PREFECT_WORK_POOL_NAME`         | Plain text                                           | Work pool name (`biocirv-staging-pool`)          |
| `DB_USER`                        | Plain text                                           | Cloud SQL username                               |
| `POSTGRES_DB`                    | Plain text                                           | Database name                                    |
| `DB_PASS`                        | Secret Manager (`biocirv-staging-db-password`)       | Database password                                |
| `INSTANCE_CONNECTION_NAME`       | Plain text                                           | Cloud SQL Unix socket path                       |
| `USDA_NASS_API_KEY`              | Secret Manager (`biocirv-staging-usda-nass-api-key`) | USDA NASS QuickStats API key                     |
| `CREDENTIALS_PATH`               | Plain text                                           | Path to GSheets/Drive service account file       |
| `GOOGLE_APPLICATION_CREDENTIALS` | Plain text                                           | Path to GCP service account credentials (ADC)    |
| `LANDIQ_SHAPEFILE_URL`           | Plain text                                           | HTTP URL to download LandIQ shapefile at runtime |

---

## Secret Management

### Automatically managed by Pulumi

| Secret                                | Description                                       |
| ------------------------------------- | ------------------------------------------------- |
| `biocirv-staging-db-password`         | Cloud SQL primary user password (auto-generated)  |
| `biocirv-staging-postgres-password`   | Postgres superuser password (auto-generated)      |
| `biocirv-staging-ro-biocirv_readonly` | Read-only user password (auto-generated)          |
| `biocirv-staging-prefect-auth`        | Prefect HTTP Basic Auth password (auto-generated) |

### Manually uploaded post-deploy

| Secret                                | How to upload                                                                                  |
| ------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `biocirv-staging-gsheets-credentials` | `gcloud secrets versions add biocirv-staging-gsheets-credentials --data-file=credentials.json` |
| `biocirv-staging-usda-nass-api-key`   | `echo -n "KEY" \| gcloud secrets versions add biocirv-staging-usda-nass-api-key --data-file=-` |

---

## ETL Flow Troubleshooting

#### ETL flow fails with "USDA API key is empty"

Upload the USDA NASS API key to Secret Manager:

```bash
echo -n "YOUR_USDA_NASS_API_KEY" | \
  gcloud secrets versions add biocirv-staging-usda-nass-api-key \
  --data-file=- --project=biocirv-470318
```

Then force a new Cloud Run revision:

```bash
gcloud run services update biocirv-prefect-worker \
  --image=gcr.io/biocirv-470318/pipeline:latest --region=us-west1
```

#### Google Sheets / Drive authentication fails

1. Verify the secret has a version:
   `gcloud secrets versions list biocirv-staging-gsheets-credentials`
2. Verify `CREDENTIALS_PATH` env var on the worker is
   `/app/gsheets-credentials/credentials.json`
3. Verify the service account in `credentials.json` has been shared on the
   relevant Google Sheets

#### LandIQ flow fails with "Shapefile path does not exist"

Set the `LANDIQ_SHAPEFILE_URL` env var to a valid URL pointing to a zip archive
containing the shapefile. Update via Pulumi config or override at deploy time:

```bash
# Update in cloud_run.py's LANDIQ_SHAPEFILE_URL value, then redeploy:
pixi run cloud-deploy
# Or update the running service directly:
gcloud run services update biocirv-prefect-worker \
  --update-env-vars LANDIQ_SHAPEFILE_URL=https://your-url/landiq.zip \
  --region=us-west1
```

#### Worker not picking up new code after image rebuild

Pulumi pins image digests and won't detect `:latest` tag updates automatically.
Force a new revision:

```bash
gcloud run services update biocirv-prefect-worker \
  --image=gcr.io/biocirv-470318/pipeline:latest --region=us-west1
```
