import sys
from prefect import flow
from src.flows.primary_product import primary_product_flow
from src.flows.analysis_type import analysis_type_flow

# A dictionary mapping flow names to their function objects
AVAILABLE_FLOWS = {
    "primary_product": primary_product_flow,
    "analysis_type": analysis_type_flow,
}

@flow(name="Master ETL Flow", log_prints=True)
def master_flow():
    """
    A master flow to orchestrate all ETL pipelines.
    """
    print("Running master ETL flow...")
    for flow_name, flow_func in AVAILABLE_FLOWS.items():
        print(f"--- Running sub-flow: {flow_name} ---")
        flow_func()
    print("Master ETL flow completed.")

if __name__ == "__main__":
    # This script is a placeholder for running flows directly.
    # Deployments are now managed via the 'prefect.yaml' file and the 'prefect deploy' command.
    print("This script is not intended for creating deployments.")
    print("To deploy, run the following command from within the container:")
    print("\n  prefect deploy\n")
    print("To run the flow directly for testing (using a temporary server), run:")
    print("\n  python -c 'from run_prefect_flow import master_flow; master_flow()'\n")
