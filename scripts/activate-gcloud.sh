#!/bin/sh
# Add Google Cloud SDK to PATH if installed in the pixi environment
if [ -d "$CONDA_PREFIX/google-cloud-sdk/bin" ]; then
    export PATH="$CONDA_PREFIX/google-cloud-sdk/bin:$PATH"
fi

# Set project via env var (process-scoped, doesn't mutate global gcloud config)
if [ -z "$CLOUDSDK_CORE_PROJECT" ]; then
    export CLOUDSDK_CORE_PROJECT="biocirv-470318"
fi
