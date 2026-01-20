from prefect import flow
from ca_biositing.pipeline.etl.extract import proximate, ultimate, cmpana

# Import the new tasks
from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
from ca_biositing.pipeline.etl.transform.analysis.proximate_record import transform_proximate_record
from ca_biositing.pipeline.etl.transform.analysis.ultimate_record import transform_ultimate_record
from ca_biositing.pipeline.etl.transform.analysis.compositional_record import transform_compositional_record

from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
from ca_biositing.pipeline.etl.load.analysis.proximate_record import load_proximate_record
from ca_biositing.pipeline.etl.load.analysis.ultimate_record import load_ultimate_record
from ca_biositing.pipeline.etl.load.analysis.compositional_record import load_compositional_record

@flow(name="Analysis Records ETL", log_prints=True)
def analysis_records_flow():
    """
    Orchestrates the ETL process for Proximate, Ultimate, and Compositional records,
    including their associated observations.
    """
    print("Starting Analysis Records ETL flow...")

    # 1. Extract
    prox_raw = proximate.extract()
    ult_raw = ultimate.extract()
    cmpana_raw = cmpana.extract()

    raw_data = [prox_raw, ult_raw, cmpana_raw]

    # 2. Transform (Now includes cleaning, coercion, and normalization)
    obs_df = transform_observation(raw_data)

    # Assuming order: 0: Proximate, 1: Ultimate, 2: Compositional
    prox_rec_df = transform_proximate_record(prox_raw)
    ult_rec_df = transform_ultimate_record(ult_raw)
    comp_rec_df = transform_compositional_record(cmpana_raw)

    # 3. Load
    load_observation(obs_df)
    load_proximate_record(prox_rec_df)
    load_ultimate_record(ult_rec_df)
    load_compositional_record(comp_rec_df)

    print("Analysis Records ETL flow completed successfully.")

if __name__ == "__main__":
    analysis_records_flow()
