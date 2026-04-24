from prefect import flow


@flow(name="Qualitative ETL", log_prints=True)
def qualitative_etl_flow():
    """Orchestrate the qualitative ETL pipeline."""
    from prefect import get_run_logger

    from ca_biositing.pipeline.etl.extract.qualitative import extract_qualitative_sheets
    from ca_biositing.pipeline.etl.transform.analysis.qualitative import transform_qualitative_payloads
    from ca_biositing.pipeline.etl.load.analysis.qualitative import load_qualitative_payloads
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

    logger = get_run_logger()
    logger.info("Starting Qualitative ETL flow...")

    etl_run_id = create_etl_run_record.fn(pipeline_name="Qualitative ETL")
    lineage_group_id = create_lineage_group.fn(
        etl_run_id=etl_run_id,
        note="Qualitative market and end-use analysis",
    )

    raw_payloads = extract_qualitative_sheets()
    transformed_payloads = transform_qualitative_payloads(
        raw_payloads,
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id,
    )
    result = load_qualitative_payloads(transformed_payloads)

    logger.info("Qualitative ETL flow completed successfully.")
    return result


if __name__ == "__main__":
    qualitative_etl_flow()
