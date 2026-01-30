# Notebook Import Guide for the `ca_biositing` Project

This guide explains how to work with Jupyter notebooks (including the VS Code
Jupyter extension) in a repository that uses **PEP 420 namespace packages**.

---

## Why imports can break

The repository is split into three independent distributions that all share the
top‑level namespace `ca_biositing`:

- `src/ca_biositing/datamodels`
- `src/ca_biositing/pipeline`
- `src/ca_biositing/webservice`

Each distribution contributes a sub‑package (`datamodels`, `pipeline`,
`webservice`) to the common namespace. For Python to locate those sub‑packages,
the _distribution root_ (e.g. `src/ca_biositing/pipeline`) must be on
`PYTHONPATH`.

If you add only the generic `src` directory to `PYTHONPATH`, Python sees the
empty namespace package `ca_biositing` but cannot find the concrete
sub‑packages, resulting in an error such as:

```
ModuleNotFoundError: No module named 'ca_biositing.pipeline.utils'
```

---

## How we solve it in VS Code

A **workspace settings file** has been added at `.vscode/settings.json`:

```json
{
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/src/ca_biositing/pipeline:${workspaceFolder}/src/ca_biositing/datamodels:${workspaceFolder}/src/ca_biositing/webservice"
  },
  "python.analysis.extraPaths": [
    "${workspaceFolder}/src/ca_biositing/pipeline",
    "${workspaceFolder}/src/ca_biositing/datamodels",
    "${workspaceFolder}/src/ca_biositing/webservice"
  ],
  "jupyter.notebookFileRoot": "${workspaceFolder}"
}
```

### What this does

- **Terminals** opened from VS Code inherit `PYTHONPATH` with the three
  distribution roots.
- The **Python language server** (IntelliSense, linting) also searches those
  paths.
- The **Jupyter extension** launches notebooks with the same environment, so
  every cell sees the correct imports.

---

## Using notebooks

1. Open the repository folder in VS Code (`File → Open Folder…`).
2. Open or create a notebook (`.ipynb`).
3. In the first cell you can import directly, e.g.:
   ```python
   from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df
   ```
4. To import something from the `datamodels` package, just use its namespace:
   ```python
   from ca_biositing.datamodels.datamodels.database import engine
   ```
5. Verify that the import path is correct:
   ```python
   import sys
   print([p for p in sys.path if 'ca_biositing' in p])
   ```
   You should see the three directories listed.

---

## When you run notebooks **outside** VS Code

If you launch `jupyter notebook` or `jupyter lab` from a terminal that does not
have the workspace settings applied, you can still make the imports work by
calling a tiny helper that ships with the repo:

```python
from ca_biositing.pipeline.utils.import_helper import add_project_paths
add_project_paths()  # adjusts sys.path automatically
from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df
```

The helper walks up the file tree until it finds `pixi.toml` and adds the
correct distribution root.

---

## Summary of import paths

| Component      | Distribution root on `PYTHONPATH` | Example import                                                                 |
| -------------- | --------------------------------- | ------------------------------------------------------------------------------ |
| **Pipeline**   | `src/ca_biositing/pipeline`       | `from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df` |
| **Datamodels** | `src/ca_biositing/datamodels`     | `from ca_biositing.datamodels.datamodels.database import engine`               |
| **Webservice** | `src/ca_biositing/webservice`     | `from ca_biositing.webservice.main import app`                                 |

With the workspace settings (or the helper) in place, you can mix imports across
components without any extra fiddling.
