import sys
import traceback
from prefect import flow, get_run_logger
from prefect.utilities.importtools import import_object

# A dictionary mapping flow names to their import paths
AVAILABLE_FLOWS = {
    "primary_ag_product": "ca_biositing.pipeline.flows.primary_ag_product.primary_ag_product_flow",
    "analysis_type": "ca_biositing.pipeline.flows.analysis_type.analysis_type_flow",
}

@flow(name="Master ETL Flow", log_prints=True)
def master_flow():
    """
    A master flow to orchestrate all ETL pipelines.
    This flow dynamically imports and runs sub-flows, allowing it to continue
    even if some sub-flows fail to import or run.
    """
    logger = get_run_logger()
    logger.info("Running master ETL flow...")
    for flow_name, flow_path in AVAILABLE_FLOWS.items():
        try:
            logger.info(f"--- Running sub-flow: {flow_name} ---")
            flow_func = import_object(flow_path)
            flow_func()
        except Exception as e:
            logger.error(f"Flow '{flow_name}' failed with error: {e}")
            logger.error(traceback.format_exc())
    logger.info("Master ETL flow completed.")

if __name__ == "__main__":
    # This script is a placeholder for running flows directly.
    # Deployments are now managed via the 'prefect.yaml' file and the 'prefect deploy' command.
    print("This script is not intended for creating deployments.")
    print("To deploy, run the following command from within the container:")
    print("\n  prefect deploy\n")
    print("To run the flow directly for testing (using a temporary server), run:")
    print("\n  python -c 'from run_prefect_flow import master_flow; master_flow()'\n")
