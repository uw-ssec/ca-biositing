from prefect import flow
from src.pipeline.etl.extract.basic_sample_info import extract_basic_sample_info
from src.pipeline.etl.transform.products.primary_product import transform_products_primary_product
from src.pipeline.etl.load.products.primary_product import load_products_primary_product

@flow(name="Primary Product ETL", log_prints=True)
def primary_product_flow():
    """
    ETL flow for processing primary products.

    This flow extracts basic sample information, transforms it to identify
    unique primary products, and loads them into the database.
    """
    print("Running Primary Product ETL flow...")

    # Extract
    basic_sample_info_df = extract_basic_sample_info()

    # Transform
    # The transform function expects a dictionary of data sources.
    primary_product_df = transform_products_primary_product({"basic_sample_info": basic_sample_info_df})

    # Load
    load_products_primary_product(primary_product_df)

    print("Primary Product ETL flow completed successfully.")
