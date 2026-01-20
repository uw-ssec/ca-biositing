from prefect import flow, task
print("DEBUG: analysis_records.py module loaded")
# Move imports inside the flow to avoid module-level import hangs
# from ca_biositing.pipeline.etl.extract import proximate, ultimate, cmpana

# Import the new tasks
# Move heavy imports inside the flow to avoid module-level hangs
# from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
# from ca_biositing.pipeline.etl.transform.analysis.proximate_record import transform_proximate_record
# from ca_biositing.pipeline.etl.transform.analysis.ultimate_record import transform_ultimate_record
# from ca_biositing.pipeline.etl.transform.analysis.compositional_record import transform_compositional_record

# from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
# from ca_biositing.pipeline.etl.load.analysis.proximate_record import load_proximate_record
# from ca_biositing.pipeline.etl.load.analysis.ultimate_record import load_ultimate_record
# from ca_biositing.pipeline.etl.load.analysis.compositional_record import load_compositional_record

@flow(name="Analysis Records ETL", log_prints=True)
def analysis_records_flow(*args, **kwargs):
    """
    Orchestrates the ETL process for Proximate, Ultimate, and Compositional records,
    including their associated observations.
    """
    print(f"DEBUG: Inside analysis_records_flow with args={args} kwargs={kwargs}")
    from prefect import get_run_logger
    print("DEBUG: Importing extractors...")
    from ca_biositing.pipeline.etl.extract import proximate, ultimate, cmpana
    print("DEBUG: Importing transformers...")
    print("DEBUG: Importing transform_observation...")
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    print("DEBUG: Importing transform_proximate_record...")
    from ca_biositing.pipeline.etl.transform.analysis.proximate_record import transform_proximate_record
    print("DEBUG: Importing transform_ultimate_record...")
    from ca_biositing.pipeline.etl.transform.analysis.ultimate_record import transform_ultimate_record
    print("DEBUG: Importing transform_compositional_record...")
    from ca_biositing.pipeline.etl.transform.analysis.compositional_record import transform_compositional_record

    print("DEBUG: Importing loaders...")
    print("DEBUG: Importing load_observation...")
    # from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
    import importlib
    print("DEBUG: Using importlib for load_observation...")
    load_obs_mod = importlib.import_module("ca_biositing.pipeline.etl.load.analysis.observation")
    print("DEBUG: Module load_observation imported")
    load_observation = load_obs_mod.load_observation
    print("DEBUG: Importing load_proximate_record...")
    from ca_biositing.pipeline.etl.load.analysis.proximate_record import load_proximate_record
    print("DEBUG: Importing load_ultimate_record...")
    from ca_biositing.pipeline.etl.load.analysis.ultimate_record import load_ultimate_record
    print("DEBUG: Importing load_compositional_record...")
    from ca_biositing.pipeline.etl.load.analysis.compositional_record import load_compositional_record

    print("DEBUG: Getting logger...")
    logger = get_run_logger()
    logger.info("Starting Analysis Records ETL flow...")

    # 1. Extract
    logger.info("Extracting Proximate data...")
    prox_raw = proximate.extract.fn()
    logger.info("Extracting Ultimate data...")
    ult_raw = ultimate.extract.fn()
    logger.info("Extracting Compositional data...")
    cmpana_raw = cmpana.extract.fn()

    raw_data = [prox_raw, ult_raw, cmpana_raw]

    # 2. Transform (Now includes cleaning, coercion, and normalization)
    logger.info("Starting transformations...")

    @task(name="Wrapper Transform Observation")
    def wrap_obs(data):
        print("DEBUG: Inside wrap_obs task")
        return transform_observation.fn(data)

    print("DEBUG: Calling wrap_obs()")
    obs_df = wrap_obs(raw_data)
    print("DEBUG: wrap_obs() completed")

    # Assuming order: 0: Proximate, 1: Ultimate, 2: Compositional
    logger.info("Transforming Proximate records...")
    print("DEBUG: Calling transform_proximate_record.fn()")
    prox_rec_df = transform_proximate_record.fn(prox_raw)
    print("DEBUG: transform_proximate_record.fn() completed")

    logger.info("Transforming Ultimate records...")
    print("DEBUG: Calling transform_ultimate_record.fn()")
    ult_rec_df = transform_ultimate_record.fn(ult_raw)
    print("DEBUG: transform_ultimate_record.fn() completed")

    logger.info("Transforming Compositional records...")
    print("DEBUG: Calling transform_compositional_record.fn()")
    comp_rec_df = transform_compositional_record.fn(cmpana_raw)
    print("DEBUG: transform_compositional_record.fn() completed")

    # 3. Load
    logger.info("Starting database load...")
    load_observation.fn(obs_df)
    load_proximate_record.fn(prox_rec_df)
    load_ultimate_record.fn(ult_rec_df)
    load_compositional_record.fn(comp_rec_df)

    logger.info("Analysis Records ETL flow completed successfully.")

if __name__ == "__main__":
    analysis_records_flow()
