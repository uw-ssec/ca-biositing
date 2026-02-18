FROM prefecthq/prefect:3-python3.12

RUN pip install --no-cache-dir prefect-gcp

# The worker command is set via Cloud Run service args
CMD ["prefect", "worker", "start", "--pool", "biocirv-staging-pool", "--type", "cloud-run-v2"]
