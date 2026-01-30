# --------------------------------------------------------------
# Ensure the ca_biositing namespace packages are importable
# --------------------------------------------------------------
try:
    from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df
except ModuleNotFoundError:                     # fallback for ad‑hoc runs
    from pathlib import Path
    import sys

    # Walk up until we find pixi.toml (repo root)
    cur = Path(__file__).resolve()
    while not (cur / "pixi.toml").exists():
        cur = cur.parent
        if cur == cur.parent:
            raise FileNotFoundError("Could not locate repo root (pixi.toml)")

    # Add the three distribution roots
    for comp in ("pipeline", "datamodels", "webservice"):
        sys.path.insert(0, str(cur / "src" / "ca_biositing" / comp))

    # Now the import works
    from ca_biositing.pipeline.utils.name_id_swap import replace_name_with_id_df
# --------------------------------------------------------------
# Your regular script logic follows
# --------------------------------------------------------------
print("Import succeeded – you can now use replace_name_with_id_df")
