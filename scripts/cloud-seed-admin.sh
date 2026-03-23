#!/usr/bin/env bash
set -euo pipefail

# Execute the seed-admin Cloud Run job.
# DEPLOY_ENV defaults to "staging" if not set.

DEPLOY_ENV="${DEPLOY_ENV:-staging}"
JOB_NAME="biocirv-${DEPLOY_ENV}-seed-admin"

gcloud run jobs execute "$JOB_NAME" \
  --region=us-west1 \
  --wait
