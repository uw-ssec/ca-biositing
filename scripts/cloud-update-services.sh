#!/usr/bin/env bash
set -euo pipefail

# Force new Cloud Run revisions with IMAGE_TAG.
# IMAGE_TAG defaults to "latest" if not set in the environment.

gcloud run services update biocirv-prefect-worker \
  --image="gcr.io/biocirv-470318/pipeline:${IMAGE_TAG:-latest}" \
  --region=us-west1

gcloud run services update biocirv-webservice \
  --image="gcr.io/biocirv-470318/webservice:${IMAGE_TAG:-latest}" \
  --region=us-west1
