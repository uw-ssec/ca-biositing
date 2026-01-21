from prefect import flow

@flow(name="Land IQ ETL", log_prints=True)
def landiq_etl_flow(shapefile_path: str = None, chunk_size: int = 10000):
    """
    Orchestrates the ETL process for Land IQ geospatial data using chunking to manage memory.
    """
    from prefect import get_run_logger
    import pyogrio
    from ca_biositing.pipeline.etl.transform.landiq.landiq_record import transform_landiq_record
    from ca_biositing.pipeline.etl.load.landiq import load_landiq_record
    from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group
    from ca_biositing.pipeline.etl.extract.landiq import DEFAULT_SHAPEFILE_PATH

    logger = get_run_logger()
    logger.info("Starting Land IQ ETL flow with chunking...")

    path = shapefile_path or DEFAULT_SHAPEFILE_PATH

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record.fn(pipeline_name="Land IQ ETL")
    lineage_group_id = create_lineage_group.fn(
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
            logger.info(f"Processing chunk: {skip} to {min(skip + chunk_size, total_features)}")

            # Extract chunk
            chunk_gdf = pyogrio.read_dataframe(path, skip_features=skip, max_features=chunk_size)

            if chunk_gdf is None or chunk_gdf.empty:
                continue

            # Transform chunk
            transformed_chunk = transform_landiq_record.fn(
                chunk_gdf,
                etl_run_id=etl_run_id,
                lineage_group_id=lineage_group_id
            )

            if transformed_chunk is not None and not transformed_chunk.empty:
                # Load chunk
                load_landiq_record.fn(transformed_chunk)

            # Explicitly clear memory if possible
            del chunk_gdf
            del transformed_chunk

        logger.info("Land IQ ETL flow completed successfully.")
    except Exception as e:
        logger.error(f"Chunked processing failed: {e}", exc_info=True)

if __name__ == "__main__":
    landiq_etl_flow()
