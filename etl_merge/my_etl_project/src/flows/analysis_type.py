from prefect import flow
from src.etl.extract.experiments import extract_experiments
from src.etl.transform.analysis.analysis_type import transform_analysis_analysis_type
from src.etl.load.analysis.analysis_type import load_analysis_analysis_type

@flow(name="Analysis Type ETL", log_prints=True)
def analysis_type_flow():
    """
    ETL flow for processing analysis types.

    This flow extracts experiment data, transforms it to identify
    unique analysis types, and loads them into the database.
    """
    print("Running Analysis Type ETL flow...")

    # Extract
    experiments_df = extract_experiments()

    # Transform
    analysis_type_df = transform_analysis_analysis_type({"experiments": experiments_df})

    # Load
    load_analysis_analysis_type(analysis_type_df)

    print("Analysis Type ETL flow completed successfully.")
