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
    Orchestrates the ETL process for Proximate, Ultimate, Compositional,
    ICP, XRF, and Calorimetry records, including their associated observations.
    """
    from prefect import get_run_logger
    from ca_biositing.pipeline.etl.extract import proximate, ultimate, cmpana, icp, xrf, calorimetry
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.transform.analysis.proximate_record import transform_proximate_record
    from ca_biositing.pipeline.etl.transform.analysis.ultimate_record import transform_ultimate_record
    from ca_biositing.pipeline.etl.transform.analysis.compositional_record import transform_compositional_record
    from ca_biositing.pipeline.etl.transform.analysis.icp_record import transform_icp_record
    from ca_biositing.pipeline.etl.transform.analysis.xrf_record import transform_xrf_record
    from ca_biositing.pipeline.etl.transform.analysis.calorimetry_record import transform_calorimetry_record

    import importlib
    load_obs_mod = importlib.import_module("ca_biositing.pipeline.etl.load.analysis.observation")
    load_observation = load_obs_mod.load_observation
    from ca_biositing.pipeline.etl.load.analysis.proximate_record import load_proximate_record
    from ca_biositing.pipeline.etl.load.analysis.ultimate_record import load_ultimate_record
    from ca_biositing.pipeline.etl.load.analysis.compositional_record import load_compositional_record
    from ca_biositing.pipeline.etl.load.analysis.icp_record import load_icp_record
    from ca_biositing.pipeline.etl.load.analysis.xrf_record import load_xrf_record
    from ca_biositing.pipeline.etl.load.analysis.calorimetry_record import load_calorimetry_record

    logger = get_run_logger()
    logger.info("Starting Analysis Records ETL flow...")

    # 0. Lineage Tracking Setup
    logger.info("Setting up lineage tracking...")
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group
    etl_run_id = create_etl_run_record.fn(pipeline_name="Analysis Records ETL")
    logger.info(f"ETL Run ID: {etl_run_id}")

    lineage_group_id = create_lineage_group.fn(etl_run_id=etl_run_id, note="Analytical records (Prox, Ult, Comp, ICP, XRF, Cal)")
    logger.info(f"Lineage Group ID: {lineage_group_id}")

    # 1. Extract
    logger.info("Extracting Proximate data...")
    prox_raw = proximate.extract.fn()
    logger.info("Extracting Ultimate data...")
    ult_raw = ultimate.extract.fn()
    logger.info("Extracting Compositional data...")
    cmpana_raw = cmpana.extract.fn()
    logger.info("Extracting ICP data...")
    icp_raw = icp.extract.fn()
    logger.info("Extracting XRF data...")
    xrf_raw = xrf.extract.fn()
    logger.info("Extracting Calorimetry data...")
    cal_raw = calorimetry.extract.fn()

    raw_data = [prox_raw, ult_raw, cmpana_raw, icp_raw, xrf_raw, cal_raw]

    # 2. Transform (Now includes cleaning, coercion, and normalization)
    logger.info("Starting transformations...")

    @task(name="Wrapper Transform Observation")
    def wrap_obs(data, etl_id, lin_id):
        return transform_observation.fn(data, etl_run_id=etl_id, lineage_group_id=lin_id)

    obs_df = wrap_obs(raw_data, etl_run_id, lineage_group_id)

    logger.info("Transforming Proximate records...")
    prox_rec_df = transform_proximate_record.fn(prox_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    logger.info("Transforming Ultimate records...")
    ult_rec_df = transform_ultimate_record.fn(ult_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    logger.info("Transforming Compositional records...")
    comp_rec_df = transform_compositional_record.fn(cmpana_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    logger.info("Transforming ICP records...")
    icp_rec_df = transform_icp_record.fn(icp_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    logger.info("Transforming XRF records...")
    xrf_rec_df = transform_xrf_record.fn(xrf_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    logger.info("Transforming Calorimetry records...")
    cal_rec_df = transform_calorimetry_record.fn(cal_raw, etl_run_id=etl_run_id, lineage_group_id=lineage_group_id)

    # 3. Load
    logger.info("Starting database load...")
    load_observation.fn(obs_df)
    load_proximate_record.fn(prox_rec_df)
    load_ultimate_record.fn(ult_rec_df)
    load_compositional_record.fn(comp_rec_df)
    load_icp_record.fn(icp_rec_df)
    load_xrf_record.fn(xrf_rec_df)
    load_calorimetry_record.fn(cal_rec_df)

    logger.info("Analysis Records ETL flow completed successfully.")

if __name__ == "__main__":
    analysis_records_flow()
