import pandas as pd
from sqlmodel import Session
from database import engine
from models.experiments_analysis import AnalysisType

def load_analysis_analysis_type(analysis_types_df: pd.DataFrame):
    """
    Loads the data from the analysis_types DataFrame into the database.

    Iterates over a DataFrame and inserts each product name from the 'analysis_name' column
    into the PrimaryProduct table.
    """
    if analysis_types_df is None or analysis_types_df.empty:
        print("No data to load. Skipping database insertion.")
        return

    column_name = 'analysis_name'
    if column_name not in analysis_types_df.columns:
        print(f"Error: Column '{column_name}' not found in the DataFrame. Aborting load.")
        return

    print(f"Attempting to load {len(analysis_types_df)} analysis names into the database...")

    with Session(engine) as session:
        existing_analysis_types = session.query(AnalysisType.analysis_name).all()
        existing_analysis_type_names = {a[0] for a in existing_analysis_types}

        for analysis_type in analysis_types_df[column_name]:
            if analysis_type not in existing_analysis_type_names:
                name = AnalysisType(analysis_name=analysis_type)
                session.add(name)
                existing_analysis_type_names.add(analysis_type)
        
        session.commit()
        print("Successfully committed analysis names to the database.")
