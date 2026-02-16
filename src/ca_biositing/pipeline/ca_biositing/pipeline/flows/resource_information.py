from prefect import flow
from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

@flow(name="Resource Information ETL", log_prints=True)
def resource_information_flow():
    """
    Orchestrates the ETL process for Resource information.
    """
    # Lazy imports to avoid module-level hangs
    from ca_biositing.pipeline.etl.extract import resources
    from ca_biositing.pipeline.etl.transform import resource as resource_transform
    from ca_biositing.pipeline.etl.load import resource as resource_load
    from prefect import get_run_logger

    logger = get_run_logger()
    logger.info("Starting Resource Information ETL flow...")

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record.fn(pipeline_name="Resource Information ETL")
    lineage_group_id = create_lineage_group.fn(
        etl_run_id=etl_run_id,
        note="Resource information from resource"
    )

    # 1. Extract
    logger.info("Extracting resources info...")
    raw_df = resources.extract.fn()

    # 2. Transform
    logger.info("Transforming resource data...")
    transformed_df = resource_transform.transform.fn(
        data_sources={"resources": raw_df},
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 3. Load
    logger.info("Loading resource data...")
    resource_load.load_resource.fn(transformed_df)

    logger.info("Resource Information ETL flow completed successfully.")

if __name__ == "__main__":
    resource_information_flow()
