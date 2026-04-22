from prefect import flow
from ca_biositing.pipeline.utils.lineage import create_etl_run_record, create_lineage_group

@flow(name="Resource Information ETL", log_prints=True)
def resource_information_flow():
    """
    Orchestrates the ETL process for Resource information.

    Processes in the following order:
    1. Resources (base resource data)
    2. Resource Images (depends on Resource being loaded first)
    """
    # Lazy imports to avoid module-level hangs
    from ca_biositing.pipeline.etl.extract import resources, resource_images
    from ca_biositing.pipeline.etl.transform import resource as resource_transform
    from ca_biositing.pipeline.etl.transform.resource_information import resource_image as resource_image_transform
    from ca_biositing.pipeline.etl.load import resource as resource_load
    from ca_biositing.pipeline.etl.load.resource_information import resource_image as resource_image_load
    from prefect import get_run_logger

    logger = get_run_logger()
    logger.info("Starting Resource Information ETL flow...")

    # 0. Lineage Tracking Setup
    etl_run_id = create_etl_run_record.fn(pipeline_name="Resource Information ETL")
    lineage_group_id = create_lineage_group.fn(
        etl_run_id=etl_run_id,
        note="Resource information including resources and resource images"
    )

    # ===== RESOURCE ETL (PHASE 1) =====
    # 1. Extract Resources
    logger.info("Extracting resources info...")
    raw_resources_df = resources.extract.fn()

    # 2. Transform Resources
    logger.info("Transforming resource data...")
    transformed_resources_df = resource_transform.transform.fn(
        data_sources={"resources": raw_resources_df},
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 3. Load Resources (MUST complete before loading resource_images)
    logger.info("Loading resource data...")
    resource_load.load_resource.fn(transformed_resources_df)

    # ===== RESOURCE IMAGES ETL (PHASE 2) =====
    # Dependency: Resources must be loaded first
    # 4. Extract Resource Images
    logger.info("Extracting resource images...")
    raw_resource_images_df = resource_images.extract.fn()

    # 5. Transform Resource Images
    logger.info("Transforming resource image data...")
    transformed_resource_images_df = resource_image_transform.transform_resource_images.fn(
        data_sources={"resource_images": raw_resource_images_df},
        etl_run_id=etl_run_id,
        lineage_group_id=lineage_group_id
    )

    # 6. Load Resource Images
    logger.info("Loading resource image data...")
    resource_image_load.load_resource_images.fn(transformed_resource_images_df)

    logger.info("Resource Information ETL flow completed successfully.")

if __name__ == "__main__":
    resource_information_flow()
