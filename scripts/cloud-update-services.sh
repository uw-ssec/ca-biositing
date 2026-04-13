#!/usr/bin/env bash
set -euo pipefail

# Force new Cloud Run revisions with IMAGE_TAG.
# IMAGE_TAG defaults to "latest" if not set in the environment.
# DEPLOY_ENV defaults to "staging" if not set.

DEPLOY_ENV="${DEPLOY_ENV:-staging}"

gcloud run services update "biocirv-${DEPLOY_ENV}-prefect-worker" \
  --image="us-west1-docker.pkg.dev/biocirv-470318/ghcr-proxy/sustainability-software-lab/ca-biositing/pipeline:${IMAGE_TAG:-latest}" \
  --region=us-west1

gcloud run services update "biocirv-${DEPLOY_ENV}-webservice" \
  --image="us-west1-docker.pkg.dev/biocirv-470318/ghcr-proxy/sustainability-software-lab/ca-biositing/webservice:${IMAGE_TAG:-latest}" \
  --region=us-west1
