# Notebook Setup and Namespace Package Integration

This PR introduces a standardized workflow for using Jupyter Notebooks within
the project's PEP 420 namespace package structure.

## The Challenge: PEP 420 Namespaces

The repository is split into three independent distributions that share the
`ca_biositing` namespace:

- `src/ca_biositing/datamodels`
- `src/ca_biositing/pipeline`
- `src/ca_biositing/webservice`

For Python to correctly resolve imports like
`from ca_biositing.pipeline import ...`, the **distribution roots** must be
explicitly added to the `PYTHONPATH`.

## The Solution: Pixi-Managed Kernels

We have implemented a robust solution to automate environment configuration for
all developers:

1.  **Kernel Registration Script**: A new utility, `register_pixi_kernel.sh`,
    automates the creation of a Jupyter kernel named **"ca-biositing (Pixi)"**.
2.  **Automated PYTHONPATH**: The registered kernel automatically injects the
    correct `PYTHONPATH` (comprising all three distribution roots) into the
    Jupyter environment.
3.  **VS Code Integration**: We have updated `.vscode/settings.json` to ensure
    that the Python language server and integrated terminals also inherit these
    paths, providing a seamless "Go to Definition" and linting experience.
4.  **Import Helper**: For environments outside of VS Code, a
    `ca_biositing.pipeline.utils.import_helper` is provided to dynamically
    adjust `sys.path` at runtime.

## Benefits

- **Clean Imports**: Developers can use standard `from ca_biositing...` imports
  without complex path manipulation in every notebook.
- **Reproducibility**: The environment is managed by Pixi, ensuring that all
  developers (and CI) are using the exact same dependency versions and path
  configurations.
- **Onboarding**: New contributors can get a fully functional notebook
  environment by running a single registration script.

## Relevant Files

- `docs/notebook_setup.md`: Comprehensive guide for developers.
- `src/ca_biositing/pipeline/ca_biositing/pipeline/utils/register_pixi_kernel.sh`:
  The automation script.
- `src/ca_biositing/pipeline/ca_biositing/pipeline/utils/import_helper.py`:
  Runtime path adjustment utility.
