#!/usr/bin/env bash
set -euo pipefail

# Register the Prefect deployment and trigger the Master ETL Flow.
#
# Runs `prefect deploy` and `prefect deployment run` inside a Cloud Run job
# using the pipeline image, which has all dependencies and the flow entrypoint.
#
# Requires:
#   - gcloud authenticated with appropriate permissions
#   - DEPLOY_ENV set (default: staging)

GCP_PROJECT="${GCP_PROJECT:-biocirv-470318}"
GCP_REGION="${GCP_REGION:-us-west1}"
DEPLOY_ENV="${DEPLOY_ENV:-staging}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

AR_GHCR_BASE="us-west1-docker.pkg.dev/${GCP_PROJECT}/ghcr-proxy/sustainability-software-lab/ca-biositing"
PIPELINE_IMAGE="${AR_GHCR_BASE}/pipeline:${IMAGE_TAG}"
JOB_NAME="biocirv-${DEPLOY_ENV}-trigger-etl"
# Use the same service account as the Prefect worker (has access to internal services)
SA_ENV=$( [ "${DEPLOY_ENV}" = "production" ] && echo "prod" || echo "${DEPLOY_ENV}" )
SERVICE_ACCOUNT="biocirv-${SA_ENV}-cr-worker@${GCP_PROJECT}.iam.gserviceaccount.com"

# Discover the Prefect server URL from the Cloud Run service
PREFECT_SERVER_URL=$(gcloud run services describe "biocirv-${DEPLOY_ENV}-prefect-server" \
  --region="${GCP_REGION}" \
  --format='value(status.url)')

if [ -z "${PREFECT_SERVER_URL}" ]; then
  echo "ERROR: Could not retrieve Prefect server URL from Cloud Run."
  exit 1
fi

PREFECT_API_URL="${PREFECT_SERVER_URL}/api"
echo "Prefect API URL: ${PREFECT_API_URL}"

# Create (or update) the Cloud Run job that registers and triggers the ETL flow.
# The pipeline image already contains prefect.yaml and run_prefect_flow.py at /app.
# Common args for the Cloud Run job — VPC access is required because the
# Prefect server only accepts internal traffic.
JOB_ARGS=(
  --image="${PIPELINE_IMAGE}"
  --region="${GCP_REGION}"
  --service-account="${SERVICE_ACCOUNT}"
  --vpc-egress=all-traffic
  --network=default
  --subnet=default
  --set-env-vars="PREFECT_API_URL=${PREFECT_API_URL},PREFECT_WORK_POOL_NAME=biocirv-${DEPLOY_ENV}-pool,TZ=UTC"
  --args="sh,-c,prefect --no-prompt deploy --all && prefect deployment run 'Master ETL Flow/master-etl-deployment'"
  --max-retries=0
)

echo "Updating Cloud Run job '${JOB_NAME}'..."
gcloud run jobs update "${JOB_NAME}" "${JOB_ARGS[@]}" 2>/dev/null \
|| gcloud run jobs create "${JOB_NAME}" "${JOB_ARGS[@]}"

echo "Executing Cloud Run job '${JOB_NAME}'..."
gcloud run jobs execute "${JOB_NAME}" \
  --region="${GCP_REGION}" \
  --wait

echo "ETL flow run enqueued successfully. Monitor progress in the Prefect UI."
