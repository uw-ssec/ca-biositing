from prefect import flow, get_run_logger
from ca_biositing.pipeline.etl.extract.samplemetadata import extract as extract_metadata
from ca_biositing.pipeline.etl.extract.provider_info import extract as extract_provider
from ca_biositing.pipeline.etl.transform.field_sampling.field_sample import transform_field_sample
from ca_biositing.pipeline.etl.load.field_sample import load_field_sample
from ca_biositing.pipeline.utils.lineage import create_lineage_group, create_etl_run_record

@flow(name="Field Sample ETL")
def field_sample_etl_flow():
    logger = get_run_logger()
    logger.info("Starting Field Sample ETL flow...")

    # 1. Lineage Tracking
    etl_run_id = create_etl_run_record("Field Sample ETL")
    lineage_group_id = create_lineage_group(etl_run_id)

    # 2. Extract
    logger.info("Extracting data sources...")
    metadata_df = extract_metadata()
    provider_df = extract_provider()

    data_sources = {
        "samplemetadata": metadata_df,
        "provider_info": provider_df
    }

    # 3. Transform
    logger.info("Transforming data...")
    transformed_df = transform_field_sample(
        data_sources=data_sources,
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 4. Load
    if transformed_df is not None and not transformed_df.empty:
        logger.info("Loading data into database...")
        load_field_sample(transformed_df)
    else:
        logger.warning("No data to load.")

    logger.info("Field Sample ETL flow completed successfully.")

if __name__ == "__main__":
    field_sample_etl_flow()
