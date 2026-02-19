#!/bin/sh
# Add Google Cloud SDK to PATH if installed in the pixi environment
if [ -d "$CONDA_PREFIX/google-cloud-sdk/bin" ]; then
    export PATH="$CONDA_PREFIX/google-cloud-sdk/bin:$PATH"
fi

# Set project only if gcloud is available and no project is currently configured
if command -v gcloud >/dev/null 2>&1; then
    CURRENT_PROJECT=$(gcloud config get project 2>/dev/null)
    if [ -z "$CURRENT_PROJECT" ]; then
        PROJECT_ID="biocirv-470318"
        echo "Setting gcloud project to $PROJECT_ID..."
        gcloud config set project "$PROJECT_ID"
    fi
fi
