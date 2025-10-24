import pandas as pd
from prefect import task, get_run_logger
from sqlmodel import Session, select
from src.database import engine
from src.models.biomass import PrimaryProduct

@task
def load_products_primary_product(primary_product_df: pd.DataFrame):
    """
    Loads the data from the primary products DataFrame into the database.

    Iterates over a DataFrame and inserts each product name from the 'Primary_crop' column
    into the PrimaryProduct table.
    """
    logger = get_run_logger()
    if primary_product_df is None or primary_product_df.empty:
        logger.info("No data to load. Skipping database insertion.")
        return

    column_name = 'Primary_crop'
    if column_name not in primary_product_df.columns:
        logger.error(f"Column '{column_name}' not found in the DataFrame. Aborting load.")
        return

    logger.info(f"Attempting to load {len(primary_product_df)} products into the database...")

    with Session(engine) as session:
        statement = select(PrimaryProduct.primary_product_name)
        existing_products = session.exec(statement).all()
        existing_product_names = set(existing_products)

        records_to_add = []
        for product_name in primary_product_df[column_name]:
            if product_name not in existing_product_names:
                product = PrimaryProduct(primary_product_name=product_name)
                records_to_add.append(product)
                existing_product_names.add(product_name)  # Add to set to avoid re-adding in same batch

        if records_to_add:
            session.add_all(records_to_add)
            session.commit()
            logger.info(f"Successfully committed {len(records_to_add)} new products to the database.")
        else:
            logger.info("No new products to add. All records already exist in the database.")
