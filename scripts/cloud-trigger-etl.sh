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

# Discover the Prefect server URL from the Cloud Run service
PREFECT_SERVER_URL=$(gcloud run services describe biocirv-prefect-server \
  --region="${GCP_REGION}" \
  --format='value(status.url)')

if [ -z "${PREFECT_SERVER_URL}" ]; then
  echo "ERROR: Could not retrieve Prefect server URL from Cloud Run."
  exit 1
fi

export PREFECT_API_URL="${PREFECT_SERVER_URL}/api"
echo "Prefect API URL: ${PREFECT_API_URL}"

# Enqueue the Master ETL Flow run (fire-and-forget)
echo "Triggering Master ETL Flow..."
prefect deployment run 'Master ETL Flow/master-etl-deployment'
echo "ETL flow run enqueued successfully. Monitor progress in the Prefect UI."
