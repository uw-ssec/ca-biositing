from ca_biositing.datamodels.database import engine
from sqlalchemy import text

def run_query(query, title):
    print(f"\n--- {title} ---")
    with engine.connect() as conn:
        result = conn.execute(text(query))
        rows = result.fetchall()
        for row in rows:
            print(row)

if __name__ == "__main__":
    # Check record_types in observations
    run_query("SELECT DISTINCT record_type FROM general_analysis.observation", "Observation record_types")

    # Check a few records from each analysis table to see their IDs and QC status
    run_query("SELECT record_id, resource_id, qc_pass FROM aim1_records.compositional_record LIMIT 5", "Compositional Records")
    run_query("SELECT record_id, resource_id, qc_pass FROM aim1_records.proximate_record LIMIT 5", "Proximate Records")

    # Check mapping in resource_analysis_map (simulated via SQL)
    run_query("""
        SELECT 'compositional analysis' as type, record_id FROM aim1_records.compositional_record WHERE qc_pass != 'fail' LIMIT 5
    """, "Simulated Map Sample")
