#!/usr/bin/env bash
# Register the Pixi-managed Python interpreter as a Jupyter kernel.
# This script should be run from the repository root.
# It uses the 'kernel' feature defined in pixi.toml, which includes
# jupyter, ipykernel and ipython.

# Exit on any error
set -e

# Ensure Pixi environment is installed (run `pixi install` first if needed)
# Then register the kernel with a friendly display name.

pixi run python -m ipykernel install \
    --user \
    --name=ca-biositing-pixi \
    --display-name "ca-biositing (Pixi)" \
    --env PYTHONPATH "${PWD}/src/ca_biositing/pipeline:${PWD}/src/ca_biositing/datamodels:${PWD}/src/ca_biositing/webservice"

echo "Kernel 'ca-biositing (Pixi)' registered."
# After this, open VS Code, open a notebook, and select the new kernel
