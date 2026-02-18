#!/bin/sh
# Add Google Cloud SDK to PATH if installed in the pixi environment
if [ -d "$CONDA_PREFIX/google-cloud-sdk/bin" ]; then
    export PATH="$CONDA_PREFIX/google-cloud-sdk/bin:$PATH"
fi

# Set project (only if gcloud is available)
if command -v gcloud >/dev/null 2>&1; then
    PROJECT_ID="biocirv-470318"
    echo "Setting gcloud project to $PROJECT_ID..."
    gcloud config set project "$PROJECT_ID"
fi
