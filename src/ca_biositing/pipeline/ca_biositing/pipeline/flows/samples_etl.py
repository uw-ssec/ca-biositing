from prefect import flow, get_run_logger
from ca_biositing.pipeline.flows.field_sample_etl import field_sample_etl_flow
from ca_biositing.pipeline.flows.prepared_sample_etl import prepared_sample_etl_flow

@flow(name="Samples ETL")
def samples_etl_flow():
    """
    Orchestrates the ETL process for both field samples and prepared samples.
    Field samples are processed first as prepared samples depend on them.
    """
    logger = get_run_logger()
    logger.info("Starting Samples ETL (Field + Prepared)...")

    logger.info("--- Running Field Sample ETL ---")
    field_sample_etl_flow()

    logger.info("--- Running Prepared Sample ETL ---")
    prepared_sample_etl_flow()

    logger.info("Samples ETL completed successfully.")

if __name__ == "__main__":
    samples_etl_flow()
