"""Convert resource_info.csv to resource_info.json."""

import csv
import json
from pathlib import Path

ASSETS_DIR = Path("resources/assets")


def convert() -> None:
    rows: list[dict[str, str]] = []
    with open(ASSETS_DIR / "resource_info.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))

    with open(ASSETS_DIR / "resource_info.json", "w") as f:
        json.dump(rows, f, indent=2)


if __name__ == "__main__":
    convert()
