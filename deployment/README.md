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

Run the following to set up your account's credentials on the CLI.

```bash
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

Make sure you are logged into gcloud:

```bash
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

| Component | Service |
|-----------|---------|
| **Webservice** (FastAPI) | Cloud Run Service |
| **Prefect Server** (UI + API) | Cloud Run Service |
| **Prefect Worker** (process type) | Cloud Run Service (internal, polls server, runs flows as subprocesses) |
| **Database** | Cloud SQL (PostgreSQL + PostGIS) |
| **Secrets** | Secret Manager (DB password, GSheets creds, Prefect auth) |

Infrastructure is managed by Pulumi (Python Automation API) with state stored in GCS.

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

Execute the Alembic migration Cloud Run Job:

```bash
gcloud run jobs execute biocirv-alembic-migrate --region=us-west1 --wait
```

Verify the execution completed:

```bash
gcloud run jobs executions list --job=biocirv-alembic-migrate --region=us-west1 --limit=1
```

### Prefect Server Access

The Prefect server is currently deployed **without** HTTP Basic Auth for staging.
This is because Prefect's WebSocket events client (required by process workers)
does not send auth headers, causing the worker to crash at startup.

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

The `biocirv_readonly` user is created by Pulumi. After migrations, grant
read-only privileges by connecting as `postgres`:

```bash
gcloud sql connect biocirv-staging --user=postgres --database=biocirv-staging
```

```sql
GRANT CONNECT ON DATABASE "biocirv-staging" TO biocirv_readonly;
GRANT USAGE ON SCHEMA public TO biocirv_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO biocirv_readonly;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO biocirv_readonly;
ALTER DEFAULT PRIVILEGES FOR ROLE biocirv_user IN SCHEMA public
    GRANT SELECT ON TABLES TO biocirv_readonly;
```

Retrieve the read-only password from Secret Manager (requires appropriate IAM
permissions).

### Staging Troubleshooting

#### Prefect worker not connecting

Check worker logs:

```bash
gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=20
```

Verify the worker can reach the Prefect server — look for connection errors.

#### Flow runs stuck in "Pending"

1. Verify the work pool (`biocirv-staging-pool`, type `process`) is online in the Prefect UI
2. Check the worker logs for errors: `gcloud run services logs read biocirv-prefect-worker --region=us-west1 --limit=20`
3. Verify the worker container has `DATABASE_URL` and `PREFECT_API_URL` set

#### Credential rotation

1. Update the secret version in Secret Manager
2. Redeploy both Prefect services to pick up the new secret:
   ```bash
   pixi run -e deployment cloud-deploy
   ```

#### PostGIS not enabled

Connect to the database and enable the extension:

```bash
gcloud sql connect biocirv-staging --user=postgres --database=biocirv-staging
```

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
```
