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

This creates a GCS bucket to store Pulumi state files. Only needs to be run
once per project.

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
