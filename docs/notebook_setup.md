# Notebook Setup Guide for **ca-biositing**

**Purpose** -- Set up Jupyter notebooks with correct imports for the PEP 420
namespace packages used in this repository.

---

## Prerequisites

| Requirement                                | Command                     | Note                          |
| ------------------------------------------ | --------------------------- | ----------------------------- |
| **Pixi** (v0.55+)                          | `pixi --version`            | Must be on `$PATH`.           |
| **Project dependencies**                   | `pixi install`              | Run from the repository root. |
| **VS Code** with the **Jupyter** extension | Install via the Marketplace | Optional but recommended.     |

---

## How it works

This project uses [pixi-kernel](https://github.com/renan-r-santos/pixi-kernel)
to provide a Jupyter kernel that runs code inside the Pixi environment. All
three namespace packages (`ca-biositing-datamodels`, `ca-biositing-pipeline`,
`ca-biositing-webservice`) are installed as editable PyPI packages via
`pixi.toml`, so they are importable without any `PYTHONPATH` configuration.

---

## Setup

1. Install the Pixi environment:

   ```bash
   pixi install
   ```

2. Open a notebook in VS Code or launch JupyterLab:

   ```bash
   pixi run jupyter lab
   ```

3. Select the **Pixi** kernel for your notebook. In VS Code, click the kernel
   picker in the notebook toolbar and choose the Pixi kernel.

4. Imports work directly:

   ```python
   from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df
   from ca_biositing.datamodels.models import Resource
   ```

---

## Why this works

The repository is split into three independent distributions that share the
top-level namespace `ca_biositing`:

- `src/ca_biositing/datamodels`
- `src/ca_biositing/pipeline`
- `src/ca_biositing/webservice`

Each distribution is installed into the Pixi environment as an editable PyPI
package (see the `[feature.*.pypi-dependencies]` sections in `pixi.toml`).
Because `pixi-kernel` runs notebook code inside the Pixi environment, Python's
import machinery can find all three namespace sub-packages without any path
manipulation.

---

## VS Code IntelliSense

The `.vscode/settings.json` file includes `python.analysis.extraPaths` so that
the Python language server can resolve imports across the namespace packages for
code completion and linting. These are IDE-only settings and do not affect
runtime behavior.

---

## Verify the import works

Create a test cell in a notebook:

```python
import sys
print("Python executable:", sys.executable)

from ca_biositing.pipeline.utils.lookup_utils import replace_name_with_id_df
print("Import succeeded")
```

Expected output:

```
Python executable: /Users/.../.pixi/envs/default/bin/python
Import succeeded
```

---

## Summary

| Step                | Command / Action                                       |
| ------------------- | ------------------------------------------------------ |
| Install environment | `pixi install`                                         |
| Select kernel       | Choose **Pixi** kernel in VS Code or JupyterLab        |
| Import packages     | Use standard imports (`from ca_biositing.pipeline...`) |
