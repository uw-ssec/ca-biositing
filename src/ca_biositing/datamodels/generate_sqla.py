import os
import subprocess
from pathlib import Path

def generate_sqla():
    """
    Generates SQLAlchemy models from LinkML schema modules.
    """
    base_dir = Path(__file__).parent
    linkml_dir = base_dir / "ca_biositing/datamodels/linkml"
    modules_dir = linkml_dir / "modules"
    output_dir = base_dir / "ca_biositing/datamodels/schemas/generated"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate for modules
    for yaml_file in modules_dir.glob("*.yaml"):
        module_name = yaml_file.stem
        output_file = output_dir / f"{module_name}.py"
        print(f"Generating {output_file} from {yaml_file}...")

        cmd = [
            "python", "-m", "linkml.generators.sqlalchemygen",
            "--no-mergeimports",
            str(yaml_file)
        ]

        with open(output_file, "w") as f:
            subprocess.run(cmd, stdout=f, check=True)

    # Generate for main schema
    main_yaml = linkml_dir / "ca_biositing.yaml"
    main_output = output_dir / "ca_biositing.py"
    print(f"Generating {main_output} from {main_yaml}...")

    cmd = [
        "python", "-m", "linkml.generators.sqlalchemygen",
        "--no-mergeimports",
        str(main_yaml)
    ]

    with open(main_output, "w") as f:
        subprocess.run(cmd, stdout=f, check=True)

    print("Generation complete.")

if __name__ == "__main__":
    generate_sqla()
