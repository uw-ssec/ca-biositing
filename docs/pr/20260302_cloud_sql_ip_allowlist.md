# PR: Cloud SQL Public IP Allowlist via Pulumi Secrets

## Overview

This PR implements a secure, team-shareable public IP allowlist for the staging
Cloud SQL instance. By using Pulumi Stack Secrets, we can manage access for
individual developers and offices without exposing sensitive IP addresses in
plain text within the repository.

## Key Changes

### 1. Pulumi CLI Integration

- Created `deployment/cloud/gcp/infrastructure/Pulumi.yaml` to allow the
  standard Pulumi CLI to interact with the existing Automation API project. This
  is necessary for managing stack-level configuration and secrets.

### 2. Secure Configuration Management

- **Secrets**: Implemented `db_authorized_networks` as a Pulumi stack secret.
  This stores a JSON list of authorized networks (e.g.,
  `[{"name": "dev-access", "value": "<ALLOWED_IP>/32"}]`).
- **Lazy Evaluation**: Updated `deployment/cloud/gcp/infrastructure/config.py`
  to use a `get_db_authorized_networks()` function. This ensures secrets are
  fetched at runtime within the active Pulumi context rather than at module
  import time.

### 3. Infrastructure Updates

- **Cloud SQL**: Modified `deployment/cloud/gcp/infrastructure/cloud_sql.py` to
  map the authorized networks into the `DatabaseInstance` settings.
- **Automation API Sync**: Updated
  `deployment/cloud/gcp/infrastructure/deploy.py` to use `work_dir="."`. This
  ensures that the programmatic deployment correctly identifies and loads the
  local `Pulumi.staging.yaml` file and its associated secrets.

## How to Manage the Allowlist

Authorized networks are managed via the Pulumi CLI. From the
`deployment/cloud/gcp/infrastructure` directory:

```bash
# Set the allowlist (replaces existing list)
export PULUMI_CONFIG_PASSPHRASE=""
pixi run -e deployment pulumi config set --secret db_authorized_networks '[{"name":"office", "value":"<OFFICE_IP>/32"}, {"name":"dev-personal", "value":"<DEV_IP>/32"}]' --stack staging
```

## Verification Results

- **Pulumi Preview**: Confirmed that `pixi run cloud-plan` correctly retrieves
  the encrypted secrets and identifies the required changes to the Cloud SQL
  instance:

  ```text
  Diagnostics:
    Authorized networks: [{'name': 'dev-access', 'value': '<ALLOWED_IP>/32'}]

  ~ gcp:sql:DatabaseInstance staging-db-instance update [diff: ~settings]
  ```

- **Team Consistency**: Verified that if the secret is missing, it defaults to
  an empty list, maintaining a "fail-closed" security posture.
