# Notebook Setup and Namespace Package Integration

> **Note (Phase 10/11 update):** The PYTHONPATH manipulation, `register_pixi_kernel.sh`,
> `import_helper.py`, and `universal_import_helper.py` described in the original
> version of this document have been removed. The current approach uses `pixi-kernel`
> and editable PyPI installs. See `docs/notebook_setup.md` for the current guide.

## Current Setup

The repository uses three namespace packages installed as editable PyPI
dependencies via `pixi.toml`. No `PYTHONPATH` manipulation is needed.

### Jupyter Integration

- **pixi-kernel** (PyPI package) provides a Jupyter kernel that runs code
  inside the pixi environment natively
- All three namespace packages (`datamodels`, `pipeline`, `webservice`) are
  available via standard imports: `from ca_biositing.pipeline import ...`

### VS Code Integration

- `python.analysis.extraPaths` in `.vscode/settings.json` provides IntelliSense
  support (IDE-only, does not affect runtime)

### Notebooks

Notebooks have been moved out of the shipped codebase into documentation directories:

- **Tutorials:** `src/ca_biositing/pipeline/docs/tutorials/`
- **Dev references:** `src/ca_biositing/pipeline/docs/dev-references/`

## Relevant Files

- `docs/notebook_setup.md`: Comprehensive setup guide for developers.
- `pixi.toml`: Defines editable PyPI installs and `pixi-kernel` dependency.
