from prefect import flow, get_run_logger
from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

@flow(name="County Ag Report ETL", log_prints=True)
def county_ag_report_flow():
    """
    Orchestrates the ETL process for County Agricultural Reports.

    Processes in the following order:
    1. Extract from all 3 sheets
    2. Data Source ETL (if needed)
    3. Dataset ETL (County specific)
    4. Transform to CountyAgReportRecord
    5. Load CountyAgReportRecord
    6. Transform to Observation (production/value)
    7. Load Observation
    """
    # Lazy imports to avoid module-level hangs
    from ca_biositing.pipeline.etl.extract import county_ag_report
    from ca_biositing.pipeline.etl.transform.analysis import data_source as ds_transform
    from ca_biositing.pipeline.etl.transform.analysis import county_ag_datasets as dataset_transform
    from ca_biositing.pipeline.etl.transform.analysis import county_ag_report_record as record_transform
    from ca_biositing.pipeline.etl.transform.analysis import county_ag_report_observation as observation_transform
    from ca_biositing.pipeline.etl.load.analysis import data_source as ds_load
    from ca_biositing.pipeline.etl.load.analysis import county_ag_datasets as dataset_load
    from ca_biositing.pipeline.etl.load.analysis import county_ag_report_record as record_load
    from ca_biositing.pipeline.etl.load.analysis import observation as observation_load

    logger = get_run_logger()
    logger.info("Starting County Ag Report ETL flow...")

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record.fn(pipeline_name="County Ag Report ETL")
    lineage_group_id = create_lineage_group.fn(
        etl_run_id=etl_run_id,
        note="County Ag Report data for Merced, San Joaquin, and Stanislaus (2023-2024)"
    )

    # 1. Extract
    logger.info("Extracting data from Google Sheets...")
    raw_meta = county_ag_report.primary_products.fn()
    raw_metrics = county_ag_report.pp_production_value.fn()
    raw_sources = county_ag_report.pp_data_sources.fn()

    # 2. Data Sources ETL (PREREQUISITE)
    logger.info("Transforming data sources...")
    transformed_ds_df = ds_transform.transform_data_sources.fn(
        data_sources={"pp_data_sources": raw_sources},
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )
    logger.info("Loading data sources...")
    ds_load.load_data_sources.fn(transformed_ds_df)

    # 3. Datasets ETL
    logger.info("Transforming datasets...")
    transformed_dataset_df = dataset_transform.transform_county_ag_datasets.fn(
        data_sources={"pp_data_sources": raw_sources},
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )
    logger.info("Loading datasets...")
    dataset_load.load_county_ag_datasets.fn(transformed_dataset_df)

    # 4. Transform Records
    logger.info("Transforming base records...")
    transformed_records_df = record_transform.transform_county_ag_report_records.fn(
        data_sources={
            "primary_products": raw_meta,
            "pp_production_value": raw_metrics
        },
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 5. Load Records (MUST complete before observations due to FK)
    logger.info("Loading base records...")
    record_load.load_county_ag_report_records.fn(transformed_records_df)

    # 6. Transform Observations
    logger.info("Transforming observations...")
    transformed_observations_df = observation_transform.transform_county_ag_report_observations.fn(
        data_sources={
            "pp_production_value": raw_metrics
        },
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 7. Load Observations
    logger.info("Loading observations...")
    observation_load.load_observation.fn(transformed_observations_df)

    logger.info("County Ag Report ETL flow completed successfully.")

if __name__ == "__main__":
    county_ag_report_flow()
