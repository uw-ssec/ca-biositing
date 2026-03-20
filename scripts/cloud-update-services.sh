#!/usr/bin/env bash
set -euo pipefail

# Force new Cloud Run revisions with IMAGE_TAG.
# IMAGE_TAG defaults to "latest" if not set in the environment.

gcloud run services update biocirv-prefect-worker \
  --image="ghcr.io/sustainability-software-lab/ca-biositing/pipeline:${IMAGE_TAG:-latest}" \
  --region=us-west1

gcloud run services update biocirv-webservice \
  --image="ghcr.io/sustainability-software-lab/ca-biositing/webservice:${IMAGE_TAG:-latest}" \
  --region=us-west1
