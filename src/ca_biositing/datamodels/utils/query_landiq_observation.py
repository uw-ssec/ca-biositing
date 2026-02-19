from sqlalchemy import select
from ca_biositing.datamodels.models import LandiqRecord, Observation

def generate_query():
    """
    Generates a SQL query joining LandiqRecord and Observation tables.
    """
    # Create the select statement
    # We select from LandiqRecord and join Observation
    # The join condition is explicitly specified as requested:
    # observation.record_id = landiq_record.id
    stmt = select(LandiqRecord, Observation).join(
        Observation,
        Observation.record_id == LandiqRecord.id
    )

    return stmt

if __name__ == "__main__":
    query = generate_query()
    print("Generated SQL Query:")
    print(query)
