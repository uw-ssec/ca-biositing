from prefect import flow
from ca_biositing.pipeline.etl.extract.basic_sample_info import extract_basic_sample_info
from ca_biositing.pipeline.etl.transform.products.primary_ag_product import transform_products_primary_ag_product
from ca_biositing.pipeline.etl.load.products.primary_ag_product import load_products_primary_ag_product

@flow(name="Primary Ag Product ETL", log_prints=True)
def primary_ag_product_flow():
    """
    ETL flow for processing primary agricultural products data.

    This flow extracts basic sample information, transforms it to identify
    unique primary agricultural products, and loads them into the database.
    """
    print("Running Primary Ag Product ETL flow...")

    # Extract
    basic_sample_info_df = extract_basic_sample_info()

    # Transform
    # The transform function expects a dictionary of data sources.
    primary_ag_product_df = transform_products_primary_ag_product({"basic_sample_info": basic_sample_info_df})

    # Load
    load_products_primary_ag_product(primary_ag_product_df)

    print("Primary Ag Product ETL flow completed successfully.")
