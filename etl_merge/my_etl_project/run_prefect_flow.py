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
    # Get the flow names from the command-line arguments
    flows_to_run = sys.argv[1:]

    if not flows_to_run:
        # If no arguments are provided, run the master flow
        print("No specific flow requested, running the master flow...")
        master_flow()
    else:
        # Otherwise, run the specified flows
        for flow_name in flows_to_run:
            if flow_name in AVAILABLE_FLOWS:
                print(f"Running specified flow: {flow_name}")
                AVAILABLE_FLOWS[flow_name]()
            else:
                print(f"Error: Flow '{flow_name}' not found.")
                print("Available flows are:", ", ".join(AVAILABLE_FLOWS.keys()))
