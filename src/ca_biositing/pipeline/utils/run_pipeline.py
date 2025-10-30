import sys
import os
import importlib
from typing import Callable, Optional, Dict, List
import pandas as pd

# Add the project's 'src' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

def run_etl_pipeline(
    extract_funcs: Dict[str, Callable[[], Optional[pd.DataFrame]]],
    transform_func: Callable[[Dict[str, pd.DataFrame]], Optional[pd.DataFrame]],
    load_func: Callable[[pd.DataFrame], None],
    pipeline_name: str,
    data_cache: Dict[str, pd.DataFrame]
):
    """
    Generic function to run an ETL pipeline for a specific data entity.
    """
    print(f"--- Starting {pipeline_name} ETL Pipeline ---")

    # --- 1. EXTRACT ---
    try:
        data_sources = {}
        for source_name, extract_func in extract_funcs.items():
            if source_name not in data_cache:
                print(f"Cache miss for '{source_name}'. Running extraction.")
                data_cache[source_name] = extract_func()
            else:
                print(f"Cache hit for '{source_name}'. Using cached data.")

            if data_cache[source_name] is None:
                raise RuntimeError(f"Extraction failed for source: {source_name}")

            data_sources[source_name] = data_cache[source_name]
    except RuntimeError as e:
        print(f"Pipeline '{pipeline_name}' finished with errors: {e}")
        return

    # --- 2. TRANSFORM ---
    transformed_df = transform_func(data_sources)
    if transformed_df is None:
        print(f"Pipeline '{pipeline_name}' finished with errors: Transformation failed.")
        return

    # --- 3. LOAD ---
    load_func(transformed_df)

    print(f"--- {pipeline_name} ETL Pipeline Finished Successfully ---")

def discover_and_run_pipelines(pipeline_to_run: Optional[str] = None):
    """
    Dynamically discovers and runs ETL pipelines based on file structure.
    Caches extractions to avoid redundant data fetching.
    """
    data_cache = {}
    etl_base_path = 'etl'
    transform_dir = 'src/etl/transform'

    # Recursively discover pipelines
    discovered_pipelines = []
    for root, _, files in os.walk(transform_dir):
        for filename in files:
            if filename.endswith('.py') and not filename.startswith('__'):
                # Construct the hierarchical pipeline name
                relative_path = os.path.relpath(root, transform_dir)
                if relative_path == '.':
                    pipeline_name = filename[:-3]
                else:
                    pipeline_name = os.path.join(relative_path, filename[:-3]).replace(os.sep, '.')
                discovered_pipelines.append(pipeline_name)

    if not discovered_pipelines:
        print("No pipelines found in 'src/etl/transform'.")
        return

    pipelines_to_execute = [pipeline_to_run] if pipeline_to_run else discovered_pipelines

    if pipeline_to_run and pipeline_to_run not in discovered_pipelines:
        print(f"Error: Pipeline '{pipeline_to_run}' not found.")
        print("Available pipelines:", ", ".join(discovered_pipelines))
        sys.exit(1)

    print(f"Executing pipelines: {', '.join(pipelines_to_execute)}")

    for name in pipelines_to_execute:
        run_single_pipeline(name, etl_base_path, data_cache)

def run_single_pipeline(pipeline_name: str, base_path: str, data_cache: Dict):
    """
    Dynamically imports and runs the functions for a single pipeline.
    """
    try:
        # Construct module paths for dynamic import
        transform_module_path = f"{base_path}.transform.{pipeline_name}"
        load_module_path = f"{base_path}.load.{pipeline_name}"

        transform_module = importlib.import_module(transform_module_path)
        load_module = importlib.import_module(load_module_path)

        extract_sources: List[str] = getattr(transform_module, 'EXTRACT_SOURCES')

        extract_funcs = {}
        for source in extract_sources:
            extract_module = importlib.import_module(f"{base_path}.extract.{source}")
            extract_funcs[source] = getattr(extract_module, f"extract_{source}")

        # Construct function names from the pipeline name
        func_name_suffix = pipeline_name.replace('.', '_')
        transform_func = getattr(transform_module, f"transform_{func_name_suffix}")
        load_func = getattr(load_module, f"load_{func_name_suffix}")

        run_etl_pipeline(
            extract_funcs=extract_funcs,
            transform_func=transform_func,
            load_func=load_func,
            pipeline_name=pipeline_name.replace('_', ' ').title(),
            data_cache=data_cache
        )

    except (ImportError, AttributeError, TypeError) as e:
        print(f"\n--- ERROR: Could not load or run pipeline '{pipeline_name}' ---")
        print(f"DETAILS: {e}")
        # Provide more detailed guidance
        print("Please ensure the following conventions are met:")
        print(f"1. Transform module exists: 'src/etl/transform/{pipeline_name.replace('.', '/')}.py'")
        print(f"2. Load module exists: 'src/etl/load/{pipeline_name.replace('.', '/')}.py'")
        print(f"3. The transform module has a list named 'EXTRACT_SOURCES'.")
        print(f"4. For each source in 'EXTRACT_SOURCES' (e.g., 'source_name'), a file 'src/etl/extract/source_name.py' exists.")
        print(f"5. Function names match the convention: 'transform_{pipeline_name.replace('.', '_')}' and 'load_{pipeline_name.replace('.', '_')}'.")
        print("---")

def main():
    """
    Main entry point for the script.
    Usage: python run_pipeline.py [pipeline_name]
    """
    pipeline_arg = sys.argv[1] if len(sys.argv) > 1 else None
    discover_and_run_pipelines(pipeline_arg)

if __name__ == "__main__":
    main()
