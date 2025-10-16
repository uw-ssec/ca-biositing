import pandas as pd
from prefect import task
from sqlmodel import Session
from src.database import engine
from src.models.biomass import PrimaryProduct

@task
def load_products_primary_product(primary_product_df: pd.DataFrame):
    """
    Loads the data from the primary products DataFrame into the database.

    Iterates over a DataFrame and inserts each product name from the 'Primary_crop' column
    into the PrimaryProduct table.
    """
    if primary_product_df is None or primary_product_df.empty:
        print("No data to load. Skipping database insertion.")
        return

    column_name = 'Primary_crop'
    if column_name not in primary_product_df.columns:
        print(f"Error: Column '{column_name}' not found in the DataFrame. Aborting load.")
        return

    print(f"Attempting to load {len(primary_product_df)} products into the database...")

    with Session(engine) as session:
        existing_products = session.query(PrimaryProduct.primary_product_name).all()
        existing_product_names = {p[0] for p in existing_products}

        for product_name in primary_product_df[column_name]:
            if product_name not in existing_product_names:
                product = PrimaryProduct(primary_product_name=product_name)
                session.add(product)
                existing_product_names.add(product_name)  # Add to set to avoid re-adding in same batch

        session.commit()
        print("Successfully committed products to the database.")
