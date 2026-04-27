from prefect import flow, task
import pandas as pd
import numpy as np

@flow(name="Aim 2 Bioconversion ETL", log_prints=True)
def aim2_bioconversion_flow(*args, **kwargs):
    """
    Orchestrates the ETL process for Aim 2 Bioconversion data,
    including Pretreatment and Fermentation Records.
    """
    from prefect import get_run_logger
    from ca_biositing.pipeline.etl.extract import pretreatment_data, bioconversion_data, bioconversion_setup, bioconversion_methods
    from ca_biositing.pipeline.etl.transform.analysis.pretreatment_record import transform_pretreatment_record
    from ca_biositing.pipeline.etl.transform.analysis.fermentation_record import transform_fermentation_record
    from ca_biositing.pipeline.etl.transform.analysis.observation import transform_observation
    from ca_biositing.pipeline.etl.load.analysis.pretreatment_record import load_pretreatment_record
    from ca_biositing.pipeline.etl.load.analysis.fermentation_record import load_fermentation_record
    from ca_biositing.pipeline.etl.load.analysis.method import load_method
    from ca_biositing.pipeline.etl.load.analysis.strain import load_strain
    from ca_biositing.pipeline.etl.load.analysis.observation import load_observation
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group
    from ca_biositing.pipeline.flows.analysis_type import analysis_type_flow

    logger = get_run_logger()
    logger.info("Starting Aim 2 Bioconversion ETL flow...")

    # 0. Dependencies and Lineage Tracking Setup
    # Ensure Analysis Types exist first
    analysis_type_flow()

    etl_run_id = create_etl_run_record(pipeline_name="Aim 2 Bioconversion ETL")

    # --- PART 1: Pretreatment ---
    lineage_group_pre = create_lineage_group(
        etl_run_id=etl_run_id,
        note="Aim 2 Bioconversion - Pretreatment Records"
    )

    logger.info("Extracting Pretreatment data...")
    pretreatment_raw = pretreatment_data.extract()

    if pretreatment_raw is not None and not pretreatment_raw.empty:
        # Transform Observations
        pretreatment_raw_copy = pretreatment_raw.copy()
        pretreatment_raw_copy['analysis_type'] = 'pretreatment'
        # Ensure dataset is present for normalization
        if 'dataset' not in pretreatment_raw_copy.columns:
            pretreatment_raw_copy['dataset'] = 'biocirv'

        obs_pre_df = transform_observation(
            [pretreatment_raw_copy],
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_pre
        )
        if not obs_pre_df.empty:
            load_observation(obs_pre_df)

        # Transform Pretreatment Records
        pretreatment_rec_df = transform_pretreatment_record(
            pretreatment_raw,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_pre
        )
        if not pretreatment_rec_df.empty:
            load_pretreatment_record(pretreatment_rec_df)
    else:
        logger.warning("No Pretreatment data extracted.")

    # --- PART 2: Fermentation ---
    lineage_group_ferm = create_lineage_group(
        etl_run_id=etl_run_id,
        note="Aim 2 Bioconversion - Fermentation Records"
    )

    logger.info("Extracting Fermentation data...")
    logger.info("Extracting BioConversion Methods data...")
    methods_raw = bioconversion_methods.extract()

    if methods_raw is not None and not methods_raw.empty:
        methods_df = methods_raw.copy()
        methods_df.columns = [str(c).strip() for c in methods_df.columns]

        method_id_col = next(
            (col for col in methods_df.columns if col.lower().strip() == 'method_id'),
            None
        )

        if method_id_col is not None:
            method_load_df = pd.DataFrame({'name': methods_df[method_id_col]})
            if 'Description' in methods_df.columns:
                method_load_df['description'] = methods_df['Description']
            time_col = next(
                (col for col in methods_df.columns if col.lower().strip() == 'time_h'),
                None
            )
            if time_col is not None:
                method_load_df['duration'] = methods_df[time_col]
            load_method(method_load_df)
        else:
            logger.warning("BioConversion Methods sheet missing Method_id column; skipping method metadata load.")

    fermentation_raw = bioconversion_data.extract()
    setup_raw = bioconversion_setup.extract()

    if fermentation_raw is not None and not fermentation_raw.empty:
        # Transform Observations
        fermentation_raw_copy = fermentation_raw.copy()
        fermentation_raw_copy['analysis_type'] = 'fermentation'
        # Ensure dataset is present for normalization
        if 'dataset' not in fermentation_raw_copy.columns:
            fermentation_raw_copy['dataset'] = 'biocirv'

        obs_ferm_df = transform_observation(
            [fermentation_raw_copy],
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_ferm
        )
        if not obs_ferm_df.empty:
            load_observation(obs_ferm_df)

        # Load Strains from both setup and data sheets
        all_strains = []
        for df in [setup_raw, fermentation_raw]:
            if df is not None and not df.empty:
                for col in df.columns:
                    if col.lower().strip() in ['strain', 'strain_name', 'bioconv_method']:
                        strains = df[col].astype(str).str.strip()
                        all_strains.extend(strains.tolist())

        if all_strains:
            strains_df = pd.DataFrame({'name': all_strains})
            strains_df = strains_df.replace({"": np.nan, "nan": np.nan, "-": np.nan, "None": np.nan}).dropna()
            strains_df = strains_df.drop_duplicates()

            logger.info(f"Unique strains to load: {strains_df['name'].tolist()}")

            if not strains_df.empty:
                load_strain(strains_df)

        # Transform Fermentation Records
        fermentation_rec_df = transform_fermentation_record(
            fermentation_raw,
            etl_run_id=etl_run_id,
            lineage_group_id=lineage_group_ferm
        )
        if not fermentation_rec_df.empty:
            load_fermentation_record(fermentation_rec_df)
    else:
        logger.warning("No Fermentation data extracted.")

    logger.info("Aim 2 Bioconversion ETL flow completed successfully.")

if __name__ == "__main__":
    aim2_bioconversion_flow()
