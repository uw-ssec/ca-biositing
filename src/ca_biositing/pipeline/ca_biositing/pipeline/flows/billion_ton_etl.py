import sys
from prefect import flow, task

@task(name="Create ETL Run Record")
def create_etl_run_record_task(pipeline_name: str):
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record
    return create_etl_run_record(pipeline_name=pipeline_name)

@task(name="Create Lineage Group")
def create_lineage_group_task(etl_run_id: str, note: str):
    from ca_biositing.pipeline.utils.lineage import create_lineage_group
    return create_lineage_group(etl_run_id=etl_run_id, note=note)

@flow(name="Billion Ton ETL", log_prints=True, persist_result=False)
def billion_ton_etl_flow(
    file_id: str = "11xLy_kPTHvoqciUMy3SYA3DLCDIjkOGa",
    file_name: str = "billionton_23_agri_download.csv"
):
    """
    Orchestrates the ETL process for Billion Ton agricultural data.
    """
    from prefect import get_run_logger
    from ca_biositing.pipeline.etl.extract.billion_ton import extract
    from ca_biositing.pipeline.etl.transform.billion_ton import transform
    from ca_biositing.pipeline.etl.load.billion_ton import load

    logger = get_run_logger()

    # Force stdout to flush immediately
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

    logger.info(f"Starting Billion Ton ETL flow for file_id {file_id}...")

    # 1. Extract
    raw_df = extract(file_id=file_id, file_name=file_name)
    if raw_df is None or raw_df.empty:
        logger.error("Extraction failed or returned no data. Aborting.")
        return

    # 2. Lineage Tracking Setup
    etl_run_id = create_etl_run_record_task(pipeline_name="Billion Ton ETL")
    lineage_group_id = create_lineage_group_task(
        etl_run_id=etl_run_id,
        note="Billion Ton 2023 Agricultural Data"
    )

    # 3. Transform
    # The transform task expects a dictionary of data sources
    data_sources = {"billion_ton": raw_df}
    transformed_df = transform(
        data_sources=data_sources,
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    if transformed_df is None or transformed_df.empty:
        logger.error("Transformation failed or returned no data. Aborting.")
        return

    # 4. Load
    load(transformed_df)

    logger.info("Billion Ton ETL flow completed successfully.")

if __name__ == "__main__":
    billion_ton_etl_flow()
