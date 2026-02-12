from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract.preparation import extract as extract_preparation
from ca_biositing.pipeline.etl.transform.prepared_sample import transform as transform_prepared_sample
from ca_biositing.pipeline.etl.load.prepared_sample import load_prepared_sample
from ca_biositing.pipeline.utils.lineage import create_lineage_group, create_etl_run_record

@flow(name="Prepared Sample ETL")
def prepared_sample_etl_flow():
    logger = get_run_logger()
    logger.info("Starting Prepared Sample ETL flow...")

    # 1. Lineage Tracking
    etl_run_id = create_etl_run_record("Prepared Sample ETL")
    lineage_group_id = create_lineage_group(etl_run_id)

    # 2. Extract
    logger.info("Extracting preparation data...")
    raw_df = extract_preparation()

    if raw_df is None:
        logger.error("Extraction failed. Aborting flow.")
        return

    data_sources = {
        "preparation": raw_df
    }

    # 3. Transform
    logger.info("Transforming data...")
    transformed_df = transform_prepared_sample(
        data_sources=data_sources,
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 4. Load
    if transformed_df is not None and not transformed_df.empty:
        logger.info("Loading data into database...")
        load_prepared_sample(transformed_df)
    else:
        logger.warning("No data to load.")

    logger.info("Prepared Sample ETL flow completed successfully.")

if __name__ == "__main__":
    prepared_sample_etl_flow()
