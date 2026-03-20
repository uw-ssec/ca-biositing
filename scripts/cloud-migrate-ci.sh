#!/usr/bin/env bash
set -euo pipefail

# Update migration job image with IMAGE_TAG and execute.
# IMAGE_TAG defaults to "latest" if not set in the environment.

gcloud run jobs update biocirv-alembic-migrate \
  --image="ghcr.io/sustainability-software-lab/ca-biositing/pipeline:${IMAGE_TAG:-latest}" \
  --region=us-west1

gcloud run jobs execute biocirv-alembic-migrate \
  --region=us-west1 \
  --wait
