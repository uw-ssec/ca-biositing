#!/usr/bin/env bash
set -euo pipefail

# Update migration job image with IMAGE_TAG and execute.
# IMAGE_TAG defaults to "latest" if not set in the environment.
# DEPLOY_ENV defaults to "staging" if not set.

DEPLOY_ENV="${DEPLOY_ENV:-staging}"
JOB_NAME="biocirv-${DEPLOY_ENV}-migrate"

gcloud run jobs update "$JOB_NAME" \
  --image="us-west1-docker.pkg.dev/biocirv-470318/ghcr-proxy/sustainability-software-lab/ca-biositing/pipeline:${IMAGE_TAG:-latest}" \
  --region=us-west1

gcloud run jobs execute "$JOB_NAME" \
  --region=us-west1 \
  --wait
