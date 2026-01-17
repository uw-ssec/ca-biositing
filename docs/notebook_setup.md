# 📚 Notebook Setup Guide for **ca‑biositing**

**Purpose** – Provide a concise, step‑by‑step guide that any developer can
follow in VS Code to get Jupyter notebooks working with the correct import paths
for the PEP 420 namespace packages used in this repository.

---

## 1️⃣ Prerequisites

| Requirement                                | Command                       | Note                          |
| ------------------------------------------ | ----------------------------- | ----------------------------- |
| **Pixi** (v0.55+)                          | `pixi --version`              | Must be on `$PATH`.           |
| **Project dependencies**                   | `pixi install`                | Run from the repository root. |
| **VS Code** with the **Jupyter** extension | _Install via the Marketplace_ | Enables kernel selection.     |

---

## 2️⃣ Register the Pixi‑managed Jupyter kernel

The repository ships a helper script that creates a kernel spec with the proper
`PYTHONPATH` so that the three namespace roots are visible to Jupyter.

```bash
# From the repo root
./src/ca_biositing/pipeline/ca_biositing/pipeline/utils/register_pixi_kernel.sh
```

The script internally runs:

```bash
pixi run python -m ipykernel install \
    --user \
    --name=ca-biositing-pixi \
    --display-name "ca-biositing (Pixi)" \
    --env PYTHONPATH "${PWD}/src/ca_biositing/pipeline:${PWD}/src/ca_biositing/datamodels:${PWD}/src/ca_biositing/webservice"
```

- **Result:** a kernel spec named `ca-biositing-pixi` is written to
  `~/Library/Jupyter/kernels/ca-biositing-pixi/`.
- **File reference:**
  [`register_pixi_kernel.sh`](src/ca_biositing/pipeline/ca_biositing/pipeline/utils/register_pixi_kernel.sh:1)

> **Tip:** Re‑run the script whenever you modify the repository layout or after
> a fresh `pixi install`.

---

## 3️⃣ Reload VS Code so the kernel appears

1. Press **⇧⌘P** → _Developer: Reload Window_ (or simply restart VS Code).
2. Open any notebook inside the repo, e.g.
   [`import_test.ipynb`](src/ca_biositing/pipeline/ca_biositing/pipeline/utils/import_test.ipynb).
3. Click the kernel picker in the notebook toolbar (top‑right) and select
   **“ca‑biositing (Pixi)”**.

The notebook metadata will now contain:

```json
{
  "kernelspec": {
    "display_name": "ca-biositing (Pixi)",
    "language": "python",
    "name": "ca-biositing-pixi"
  }
}
```

---

## 4️⃣ Why imports can break

The repository is split into three independent distributions that all share the
top‑level namespace `ca_biositing`:

- `src/ca_biositing/datamodels`
- `src/ca_biositing/pipeline`
- `src/ca_biositing/webservice`

Each distribution contributes a sub‑package (`datamodels`, `pipeline`,
`webservice`) to the common namespace. For Python to locate those sub‑packages,
the **distribution root** (e.g. `src/ca_biositing/pipeline`) must be on
`PYTHONPATH`.

If you add only the generic `src` directory to `PYTHONPATH`, Python sees the
empty namespace package `ca_biositing` but cannot find the concrete
sub‑packages, resulting in an error such as:

```
ModuleNotFoundError: No module named 'ca_biositing.pipeline.utils'
```

---

## 5️⃣ VS Code workspace settings (automates the PYTHONPATH)

A workspace settings file is located at `.vscode/settings.json`:

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

**What this does**

- Terminals opened from VS Code inherit the correct `PYTHONPATH`.
- The Python language server (IntelliSense, linting) also searches those paths.
- The Jupyter extension launches notebooks with the same environment, so every
  cell sees the correct imports.

---

## 6️⃣ Verify the import works

Create a test cell (or use the existing one) in the notebook:

```python
import sys
print("Python executable:", sys.executable)

from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df
print("Import succeeded")
```

Expected output (truncated):

```
Python executable: /Users/…/.pixi/envs/default/bin/python
Import succeeded
```

If you still see `ModuleNotFoundError`, double‑check that the kernel selected is
**ca‑biositing (Pixi)** (shown in the status bar).

---

## 7️⃣ Using notebooks (inside VS Code)

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

## 8️⃣ When you run notebooks **outside** VS Code

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

## 9️⃣ Import‑path cheat‑sheet

| Context                                                   | Import statement                                                                                     | Why it works                                                                                                                                                                                          |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Inside the Pixi kernel** (or any `pixi run …` command)  | `from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df`                       | `PYTHONPATH` includes the three roots, so the top‑level `ca_biositing` namespace resolves directly.                                                                                                   |
| **Running a script with the system Python** (no Pixi env) | `from ca_biositing.pipeline.ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df` | Without the extra `PYTHONPATH`, Python only sees the first `ca_biositing` directory on `sys.path` (often `datamodels`). The double prefix forces Python to walk back into the `pipeline` sub‑package. |
| **Inside a Docker dev container** (Pixi env activated)    | Same as the Pixi kernel – short import works.                                                        | The container entrypoint runs `pixi run …`, which sets `PYTHONPATH` automatically.                                                                                                                    |

**Rule of thumb:** _If you are using the Pixi‑managed kernel (or any `pixi run`
command), always use the short import._

---

## 📋 Summary of import paths

| Component  | Distribution root on `PYTHONPATH` | Example import                                                                 |
| ---------- | --------------------------------- | ------------------------------------------------------------------------------ |
| Pipeline   | `src/ca_biositing/pipeline`       | `from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df` |
| Datamodels | `src/ca_biositing/datamodels`     | `from ca_biositing.datamodels.datamodels.database import engine`               |
| Webservice | `src/ca_biositing/webservice`     | `from ca_biositing.webservice.main import app`                                 |

---

## 🔟 Quick command‑line alternative

When you need to execute a script directly from the terminal without Jupyter,
mimic the kernel’s environment:

```bash
PYTHONPATH=$(pwd)/src/ca_biositing/pipeline:$(pwd)/src/ca_biositing/datamodels:$(pwd)/src/ca_biositing/webservice \
    pixi run python my_script.py
```

---

## 1️⃣1️⃣ Summary checklist for junior developers

1. **Install Pixi env** – `pixi install`.
2. **Register kernel** – run `register_pixi_kernel.sh`.
3. **Reload VS Code** and select the _ca‑biositing (Pixi)_ kernel.
4. **Use short imports** in notebooks and any `pixi run …` scripts.
5. **Re‑run the registration script** only if you change the repository layout
   or after a fresh `pixi install`.

---

## 🤖 LLM‑Specific Guidance for This Repository

When an LLM assists a developer with notebook or kernel issues in
_ca‑biositing_, the following concrete details are most useful:

1. **Kernel name to target** – `ca-biositing-pixi`. Any kernel‑selection
   instruction should reference this exact name so the LLM can produce a command
   like:
   ```json
   { "name": "ca-biositing-pixi" }
   ```
2. **Exact PYTHONPATH composition** – the three roots that must be present:
   ```bash
   ${PWD}/src/ca_biositing/pipeline:${PWD}/src/ca_biositing/datamodels:${PWD}/src/ca_biositing/webservice
   ```
   The LLM should embed this string when constructing kernel registration or
   when advising manual `export PYTHONPATH=…`.
3. **Workspace‑relative variables** – Always use `${workspaceFolder}` in VS Code
   settings so the paths adapt to the user’s location. For example, the JSON
   snippet in `.vscode/settings.json` must contain:
   ```json
   "${workspaceFolder}/src/ca_biositing/pipeline"
   ```
4. **Helper script location** –
   `src/ca_biositing/pipeline/ca_biositing/pipeline/utils/import_helper.py`. If
   the LLM suggests adding the helper, it should provide the import line exactly
   as:
   ```python
   from ca_biositing.pipeline.utils.import_helper import add_project_paths
   ```
5. **Common error pattern** –
   `ModuleNotFoundError: No module named 'ca_biositing.pipeline.utils'`. The LLM
   can diagnose this by checking:
   - Is the kernel `ca-biositing-pixi` active?
   - Does `.vscode/settings.json` contain the correct `PYTHONPATH`?
   - Is `add_project_paths()` called when running outside VS Code?
6. **One‑liner registration command** – The LLM can give a copy‑paste command:
   ```bash
   pixi run python -m ipykernel install \
     --user \
     --name=ca-biositing-pixi \
     --display-name "ca-biositing (Pixi)" \
     --env PYTHONPATH "$(pwd)/src/ca_biositing/pipeline:$(pwd)/src/ca_biositing/datamodels:$(pwd)/src/ca_biositing/webservice"
   ```
7. **Verification snippet** – To let the LLM instruct a quick sanity check,
   provide this cell:
   ```python
   import sys, json
   print(json.dumps({"kernel": "ca-biositing-pixi", "paths": sys.path}, indent=2))
   ```
   The output should contain the three distribution roots.
8. **Idempotent actions** – Re‑running the registration script or the
   `pixi install` command does not create duplicate kernels; the LLM should
   reassure the user that these steps are safe to repeat.
9. **Link to source** – When referencing code, always include clickable links,
   e.g.,
   [`register_pixi_kernel.sh`](src/ca_biositing/pipeline/ca_biositing/pipeline/utils/register_pixi_kernel.sh:1)
   or
   [`import_helper.py`](src/ca_biositing/pipeline/ca_biositing/pipeline/utils/import_helper.py:1).

Including these precise pointers enables an LLM to generate accurate,
repository‑specific advice without vague generalities.

---

### 🎉 All set!

Following these steps gives any developer a reproducible workflow to run
notebooks, import modules cleanly, and avoid the confusing double‑prefix import
syntax. If you encounter any issues, let me know the exact error message.
