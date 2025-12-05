# Deployment Directory

This directory contains deployment resources, specifically cloud deployment
resources, for getting the ca-biositing project up and running on Google Cloud
Platform (GCP) using OpenTofu.

# Directory Structure

```text
deployment
├── cloud/gcp/infrastructure/    # OpenTofu files
│   ├── main.tf                  # Main OpenTofu file where infra is defined
│   ├── variables.tf             # OpenTofu file supplying variables for above
```

## Quick Start

### Prerequisites

- Access to the BioCirV project in GCP
- `gcloud` CLI:
  https://docs.cloud.google.com/sdk/docs/install-sdk#latest-version

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

### Configuring OpenTofu

From the project root directory:

```bash
pixi run cloud-init
```

### Deploying Changes

From the project root directory:

```bash
# Preview pending changes
pixi run cloud-plan

# Deploy pending changes
pixi run cloud-deploy
```

### DANGEROUS: Destroy All GCP Resources

From the project root directory:

```bash
pixi run cloud-destroy
```

Certain pieces of infrastructure with deletion retention policies may fail to
delete when this is run. If you really want to delete them, change that
infrastructure's configuration in `main.tf`, deploy these changes with
`pixi run cloud-plan` and `pixi run cloud-deploy`, and then retry running the
above command.

## Troubleshooting

### Deploying architecture into a new account/project for the first time

The `google_storage_bucket` resource `terraform_state_bucket` must exist before
the OpenTofu
[backend](https://opentofu.org/docs/language/settings/backends/configuration/)
can start storing necessary state files there.

In order to set things up for the very, very first time, you'll need to

- Temporarily comment out the following lines in the `terraform` block

  ```
  backend "gcs" {
      bucket = "${var.project_id}-tf-state"
      prefix = "biocirv/state"
  }
  ```

- Deploy resources

  ```
  pixi run cloud-plan
  pixi run cloud-deploy
  ```

- Uncomment out the backend lines you commented out earlier
- Redeploy resources, saying "yes" when asked if you want to copy existing state
  to the new backend

  ```
  pixi run cloud-plan
  pixi run cloud-deploy
  ```

That should be all you need to do, and you'll never need to do it again for that
account/project!
