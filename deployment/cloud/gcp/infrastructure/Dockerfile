FROM python:3.12-slim

# Install curl for Pulumi CLI installer
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m pulumi
USER pulumi

ENV PULUMI_GCP_VERSION=9.16.0
# Install Pulumi CLI
RUN curl -fsSL https://get.pulumi.com | sh
ENV PATH="/home/pulumi/.pulumi/bin:${PATH}"

# Install Python dependencies
RUN pip install --no-cache-dir pulumi "pulumi-gcp==${PULUMI_GCP_VERSION}" pulumi-random

WORKDIR /app
