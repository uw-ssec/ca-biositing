import pandas as pd
from sqlmodel import Session, select

from ca_biositing.datamodels.database import engine
from ca_biositing.datamodels.biomass import Biomass, BiomassType
from ca_biositing.pipeline.utils.lookup_utils import replace_id_with_name_df, replace_name_with_id_df


def test_lookup_functions():
    """
    Tests the lookup utility functions for swapping IDs and names.
    """
    with Session(engine) as db:
        # 1. Load Biomass table into a DataFrame
        biomass_statement = select(Biomass)
        biomass_records = db.exec(biomass_statement).all()
        biomass_df = pd.DataFrame([record.dict() for record in biomass_records])
        print("Original Biomass DataFrame:")
        print(biomass_df.head())
        print("-" * 30)

        # 2. Test replacing ID with name
        df_with_names = replace_id_with_name_df(
            db=db,
            df=biomass_df,
            ref_model=BiomassType,
            id_column_name="biomass_type_id",
            name_column_name="biomass_type",
        )
        print("DataFrame with Biomass Type Names:")
        print(df_with_names.head())
        print("-" * 30)

        # 3. Test replacing name with ID (including 'get or create')
        # Create a dummy DataFrame with a new, non-existent biomass type
        data = {
            "biomass_name": ["Test Biomass 1", "Test Biomass 2"],
            "biomass_type": ["ag_residue", "new_test_type"],
        }
        name_df = pd.DataFrame(data)

        df_with_ids = replace_name_with_id_df(
            db=db,
            df=name_df,
            ref_model=BiomassType,
            name_column_name="biomass_type",
            id_column_name="biomass_type_id",
        )
        print("DataFrame with Biomass Type IDs (after get-or-create):")
        print(df_with_ids.head())
        print("-" * 30)

        # 4. Verify the new type was added to the database
        new_type_statement = select(BiomassType).where(
            BiomassType.biomass_type == "new_test_type"
        )
        new_type = db.exec(new_type_statement).first()
        assert new_type is not None
        print(f"Successfully verified that '{new_type.biomass_type}' was added to the database.")


if __name__ == "__main__":
    test_lookup_functions()
