#!/usr/bin/env bash
# Wrapper script for running Pulumi commands inside the ca-biositing-pulumi
# Docker container.  This exists because macOS (gRPC) crashes Pulumi Python
# directly, so we run it in a Linux container instead.
#
# Usage:
#   DEPLOY_ENV=production bash scripts/pulumi-docker.sh preview
#   DEPLOY_ENV=staging    bash scripts/pulumi-docker.sh up
#   bash scripts/pulumi-docker.sh outputs   # defaults to staging
#
# Supported commands: preview | up | destroy | refresh | outputs

set -euo pipefail

DEPLOY_ENV="${DEPLOY_ENV:-staging}"
COMMAND="${1:?Usage: pulumi-docker.sh <preview|up|destroy|refresh|outputs>}"

INFRA_DIR="deployment/cloud/gcp/infrastructure"
IMAGE="ca-biositing-pulumi"
GCLOUD_CONFIG="$HOME/.config/gcloud"

exec docker run --rm \
    -v "$PWD/${INFRA_DIR}:/app" \
    -v "${GCLOUD_CONFIG}:/home/pulumi/.config/gcloud:ro" \
    -e PULUMI_CONFIG_PASSPHRASE= \
    -e "DEPLOY_ENV=${DEPLOY_ENV}" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/home/pulumi/.config/gcloud/application_default_credentials.json \
    "${IMAGE}" \
    python deploy.py "${COMMAND}"
