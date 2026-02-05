import sys
import os
from prefect import flow, task

# Force stdout to flush immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print(f"DEBUG: Module landiq_etl loading. Python: {sys.executable}")

@task(name="Create ETL Run Record")
def create_etl_run_record_task(pipeline_name: str):
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record
    return create_etl_run_record.fn(pipeline_name=pipeline_name)

@task(name="Create Lineage Group")
def create_lineage_group_task(etl_run_id: str, note: str):
    from ca_biositing.pipeline.utils.lineage import create_lineage_group
    return create_lineage_group.fn(etl_run_id=etl_run_id, note=note)

@flow(name="Land IQ ETL", log_prints=True, persist_result=False)
def landiq_etl_flow(shapefile_path: str = "", chunk_size: int = 10000):
    sys.stdout.flush()
    print(f"DEBUG: Flow function landiq_etl_flow started. Python: {sys.executable}")
    """
    Orchestrates the ETL process for Land IQ geospatial data using chunking to manage memory.
    """
    from prefect import get_run_logger
    import os
    try:
        import pyproj
        os.environ['PROJ_LIB'] = pyproj.datadir.get_data_dir()
        import pyogrio
    except Exception:
        import pyogrio
    from ca_biositing.pipeline.etl.transform.landiq.landiq_record import transform_landiq_record
    from ca_biositing.pipeline.etl.load.landiq import load_landiq_record
    from ca_biositing.pipeline.etl.extract.landiq import DEFAULT_SHAPEFILE_PATH

    logger = get_run_logger()
    logger.info("Starting Land IQ ETL flow with chunking...")

    path = shapefile_path if shapefile_path else DEFAULT_SHAPEFILE_PATH

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record_task(pipeline_name="Land IQ ETL")
    lineage_group_id = create_lineage_group_task(
        etl_run_id=etl_run_id,
        note="Land IQ 2023 Crop Mapping (Chunked)"
    )

    # 1. Extract & Process in Chunks
    logger.info(f"Processing shapefile in chunks of {chunk_size} from {path}")

    try:
        # Get total number of features
        meta = pyogrio.read_info(path)
        total_features = meta['features']
        logger.info(f"Total features to process: {total_features}")

        for skip in range(0, total_features, chunk_size):
            print(f"DEBUG: Processing chunk: {skip}")
            logger.info(f"Processing chunk: {skip} to {min(skip + chunk_size, total_features)}")

            # Extract chunk
            chunk_gdf = pyogrio.read_dataframe(path, skip_features=skip, max_features=chunk_size)
            print(f"DEBUG: Extracted {len(chunk_gdf)} rows")

            if chunk_gdf is None or chunk_gdf.empty:
                logger.warning(f"Chunk {skip} is empty, skipping.")
                continue

            # Transform chunk
            transformed_chunk = transform_landiq_record(
                chunk_gdf,
                etl_run_id=etl_run_id,
                lineage_group_id=lineage_group_id
            )

            print(f"DEBUG: Transform returned {type(transformed_chunk)}")

            if transformed_chunk is not None and not transformed_chunk.empty:
                # Load chunk
                print("DEBUG: Calling load_landiq_record")
                load_landiq_record(transformed_chunk)
                print("DEBUG: load_landiq_record returned")
            else:
                logger.warning(f"Transformed chunk {skip} is empty or None.")

            # Explicitly clear memory if possible
            del chunk_gdf
            del transformed_chunk

        logger.info("Land IQ ETL flow completed successfully.")
    except Exception as e:
        logger.error(f"Chunked processing failed: {e}", exc_info=True)

if __name__ == "__main__":
    landiq_etl_flow()
