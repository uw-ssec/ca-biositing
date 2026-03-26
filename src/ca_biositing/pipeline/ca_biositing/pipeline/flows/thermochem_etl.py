from prefect import flow, task

@flow(name="Thermochemical Conversion ETL", log_prints=True)
def thermochem_etl_flow(*args, **kwargs):
    """
    Orchestrates the ETL process for Thermochemical Conversion data,
    including Observations and Gasification Records.
    """
    from prefect import get_run_logger
    from ca_biositing.pipeline.etl.extract import thermochem_data
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.transform.analysis.gasification_record import transform_gasification_record
    from ca_biositing.pipeline.etl.transform.analysis.experiment import transform_experiment
    from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
    from ca_biositing.pipeline.etl.load.analysis.gasification_record import load_gasification_record
    from ca_biositing.pipeline.etl.load.analysis.experiment import load_experiment
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

    logger = get_run_logger()
    logger.info("Starting Thermochemical Conversion ETL flow...")

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record(pipeline_name="Thermochemical Conversion ETL")

    lineage_group = create_lineage_group(
        etl_run_id=etl_run_id,
        note="Thermochemical Conversion - Experiments and Observations"
    )

    # 1. Extraction
    logger.info("Extracting Thermochem data...")
    thermo_exp_raw = thermochem_data.thermo_experiment()
    thermo_data_raw = thermochem_data.thermo_data()

    if thermo_data_raw is not None and not thermo_data_raw.empty:
        # --- PART 0: Experiments ---
        # First load experiments so they can be referenced by ID during normalization of records
        if thermo_exp_raw is not None and not thermo_exp_raw.empty:
            logger.info("Transforming and Loading Experiments...")
            exp_df = transform_experiment(
                raw_dfs=[thermo_exp_raw],
                etl_run_id=etl_run_id,
                lineage_group_id=lineage_group
            )
            if not exp_df.empty:
                load_experiment(exp_df)
            else:
                logger.warning("No experiments produced during transformation.")

        # --- PART 1: Observations ---
        logger.info("Transforming and Loading Observations...")
        # Prepare copy for observation transform with analysis_type and record_id
        obs_raw_copy = thermo_data_raw.copy()
        obs_raw_copy['dataset'] = 'biocirv'

        # Map record_id from Record_id as per latest source data
        if 'Record_id' in obs_raw_copy.columns:
            obs_raw_copy['record_id'] = obs_raw_copy['Record_id']
        elif 'Rx_UUID' in obs_raw_copy.columns:
            obs_raw_copy['record_id'] = obs_raw_copy['Rx_UUID']
        elif 'RxID' in obs_raw_copy.columns:
            obs_raw_copy['record_id'] = obs_raw_copy['RxID']

        # We can try to use 'analysis_type' column if it exists in the sheet,
        # otherwise default to 'gasification' as per planning
        if 'Analysis_type' not in obs_raw_copy.columns:
            obs_raw_copy['analysis_type'] = 'gasification'
        else:
            # Map Analysis_type column to lowercase for consistency if needed
            obs_raw_copy['analysis_type'] = obs_raw_copy['Analysis_type'].str.lower()

        obs_df = transform_observation(
            [obs_raw_copy],
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group
        )
        if not obs_df.empty:
            load_observation(obs_df)
        else:
            logger.warning("No observations produced during transformation.")

        # --- PART 2: Gasification Records ---
        logger.info("Transforming and Loading Gasification Records...")

        # Prepare copy for GasificationRecord transform with record_id
        gas_raw_copy = thermo_data_raw.copy()
        if 'Record_id' in gas_raw_copy.columns:
            gas_raw_copy['record_id'] = gas_raw_copy['Record_id']
        elif 'Rx_UUID' in gas_raw_copy.columns:
            gas_raw_copy['record_id'] = gas_raw_copy['Rx_UUID']
        elif 'RxID' in gas_raw_copy.columns:
            gas_raw_copy['record_id'] = gas_raw_copy['RxID']

        gas_rec_df = transform_gasification_record(
            thermo_data_df=gas_raw_copy,
            thermo_experiment_df=thermo_exp_raw,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group
        )
        if not gas_rec_df.empty:
            load_gasification_record(gas_rec_df)
        else:
            logger.warning("No gasification records produced during transformation.")

    else:
        logger.warning("No Thermochem data extracted.")

    logger.info("Thermochemical Conversion ETL flow completed successfully.")

if __name__ == "__main__":
    thermochem_etl_flow()
