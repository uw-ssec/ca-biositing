#!/usr/bin/env bash
set -euo pipefail

# Trigger the Master ETL Flow via the Prefect deployment API.
# Fire-and-forget: enqueues the run and exits. Monitor in the Prefect UI.
#
# Requires:
#   - gcloud authenticated with run.admin or run.viewer permissions
#   - prefect CLI available (pixi deployment environment)
#
# TODO: The Prefect server is currently deployed without authentication.
#       Once HTTP Basic Auth or API key auth is enabled on the server,
#       this script will need to pass credentials (e.g., via
#       PREFECT_API_KEY or PREFECT_API_AUTH_STRING).

GCP_REGION="${GCP_REGION:-us-west1}"
DEPLOY_ENV="${DEPLOY_ENV:-staging}"

# Discover the Prefect server URL from the Cloud Run service
PREFECT_SERVER_URL=$(gcloud run services describe "biocirv-${DEPLOY_ENV}-prefect-server" \
  --region="${GCP_REGION}" \
  --format='value(status.url)')

if [ -z "${PREFECT_SERVER_URL}" ]; then
  echo "ERROR: Could not retrieve Prefect server URL from Cloud Run."
  exit 1
fi

export PREFECT_API_URL="${PREFECT_SERVER_URL}/api"
echo "Prefect API URL: ${PREFECT_API_URL}"

# Register (or update) the deployment with the Prefect server.
# The prefect.yaml lives in resources/prefect/ alongside the flow entrypoint.
# This is idempotent — re-running just updates the existing deployment.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
echo "Registering Prefect deployment..."
prefect --no-prompt deploy --all --prefect-file "${REPO_ROOT}/resources/prefect/prefect.yaml"

# Enqueue the Master ETL Flow run (fire-and-forget)
echo "Triggering Master ETL Flow..."
prefect deployment run 'Master ETL Flow/master-etl-deployment'
echo "ETL flow run enqueued successfully. Monitor progress in the Prefect UI."
