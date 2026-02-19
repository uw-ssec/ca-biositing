#!/usr/bin/env bash
# Install pgschema CLI binary into the pixi environment.
# See https://www.pgschema.com/installation#pre-built-binary
set -euo pipefail

PGSCHEMA_VERSION="1.6.2"

ARCH=$(uname -m)
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

case "$ARCH" in
  arm64|aarch64) ARCH="arm64" ;;
  x86_64|amd64)  ARCH="amd64" ;;
  *) echo "Unsupported architecture: $ARCH" && exit 1 ;;
esac

DEST="${CONDA_PREFIX}/bin/pgschema"
URL="https://github.com/pgplex/pgschema/releases/download/v${PGSCHEMA_VERSION}/pgschema-${PGSCHEMA_VERSION}-${OS}-${ARCH}"

echo "Downloading pgschema v${PGSCHEMA_VERSION} for ${OS}-${ARCH}..."
curl -fSL "$URL" -o "$DEST"
chmod +x "$DEST"
echo "Installed pgschema v${PGSCHEMA_VERSION} to $DEST"
