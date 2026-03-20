#!/usr/bin/env bash
set -euo pipefail

# Build and push Docker images to GCR with IMAGE_TAG substitution.
# IMAGE_TAG defaults to "latest" if not set in the environment.

gcloud builds submit \
  --config=deployment/cloud/gcp/cloudbuild-ci.yaml \
  --substitutions="_IMAGE_TAG=${IMAGE_TAG:-latest}" \
  --project=biocirv-470318 \
  .
