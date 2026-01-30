'''Utility to configure PYTHONPATH for notebooks in the ca_biositing project.

This module provides a single function ``add_project_paths()`` that walks up the
filesystem until it finds the repository root (the directory containing
``pixi.toml``) and then inserts the appropriate distribution root for the
``ca_biositing.pipeline`` package onto ``sys.path``.

Typical usage in a notebook::

    from ca_biositing.pipeline.utils.import_helper import add_project_paths
    add_project_paths()
    from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df

The function is safe to call multiple times – it will only add the path if it is
not already present.
'''

import sys
import pathlib

def add_project_paths() -> None:
    """Add the ``ca_biositing.pipeline`` distribution root to ``sys.path``.

    The repository uses PEP 420 namespace packages, so the *distribution root*
    ``src/ca_biositing/pipeline`` must be on ``PYTHONPATH`` for imports such as
    ``ca_biositing.pipeline.utils`` to work.  This helper discovers the project
    root by locating ``pixi.toml`` and then adds the appropriate directory.
    """
    # Start at the location of this file and walk upwards until we find pixi.toml
    current = pathlib.Path(__file__).resolve()
    while not (current / "pixi.toml").exists():
        if current.parent == current:
            raise FileNotFoundError("Could not locate pixi.toml – are you inside the ca_biositing repo?")
        current = current.parent
    # The pipeline distribution root is ``src/ca_biositing/pipeline`` relative to the repo root
    pipeline_root = current / "src" / "ca_biositing" / "pipeline"
    if str(pipeline_root) not in sys.path:
        sys.path.insert(0, str(pipeline_root))
