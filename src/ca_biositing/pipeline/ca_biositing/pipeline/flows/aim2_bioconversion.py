from prefect import flow, task

@flow(name="Aim 2 Bioconversion ETL", log_prints=True)
def aim2_bioconversion_flow(*args, **kwargs):
    """
    Orchestrates the ETL process for Aim 2 Bioconversion data,
    starting with Pretreatment Records.
    """
    from prefect import get_run_logger
    from ca_biositing.pipeline.etl.extract import pretreatment_data
    from ca_biositing.pipeline.etl.transform.analysis.pretreatment_record import transform_pretreatment_record
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.load.analysis.pretreatment_record import load_pretreatment_record
    from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

    logger = get_run_logger()
    logger.info("Starting Aim 2 Bioconversion ETL flow...")

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record(pipeline_name="Aim 2 Bioconversion ETL")
    lineage_group_id = create_lineage_group(
        etl_run_id=etl_run_id,
        note="Aim 2 Bioconversion - Pretreatment Records"
    )

    # 1. Extract
    logger.info("Extracting Pretreatment data...")
    pretreatment_raw = pretreatment_data.extract()

    if pretreatment_raw is None or pretreatment_raw.empty:
        logger.warning("No Pretreatment data extracted. Skipping transform and load.")
        return

    # 2. Transform
    logger.info("Transforming Observation records...")
    # We need to add analysis_type to the raw data so observation transform knows what it is
    pretreatment_raw_copy = pretreatment_raw.copy()
    pretreatment_raw_copy['analysis_type'] = 'pretreatment'

    obs_df = transform_observation(
        [pretreatment_raw_copy],
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    logger.info("Transforming Pretreatment records...")
    pretreatment_rec_df = transform_pretreatment_record(
        pretreatment_raw,
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 3. Load
    if not obs_df.empty:
        logger.info("Loading Observations into database...")
        load_observation(obs_df)

    if not pretreatment_rec_df.empty:
        logger.info("Loading Pretreatment records into database...")
        load_pretreatment_record(pretreatment_rec_df)
    else:
        logger.warning("Pretreatment transformation resulted in empty DataFrame. Skipping load.")

    logger.info("Aim 2 Bioconversion ETL flow completed successfully.")

if __name__ == "__main__":
    aim2_bioconversion_flow()
