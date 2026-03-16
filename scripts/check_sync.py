
import os
from ca_biositing.datamodels.database import get_engine
from sqlalchemy import text

def check_sync():
    os.environ['POSTGRES_HOST'] = 'localhost'
    engine = get_engine()

    tables = {
        'proximate_record': 'proximate analysis',
        'ultimate_record': 'ultimate analysis',
        'compositional_record': 'compositional analysis',
        'icp_record': 'icp analysis',
        'xrf_record': 'xrf analysis',
        'calorimetry_record': 'calorimetry analysis',
        'xrd_record': 'xrd analysis'
    }

    with engine.connect() as conn:
        print(f"{'Analysis Type':<25} | {'Records':<10} | {'Observations':<15}")
        print("-" * 55)
        for table, record_type in tables.items():
            try:
                rec_count = conn.execute(text(f"SELECT COUNT(*) FROM public.{table}")).scalar()
                obs_count = conn.execute(text(f"SELECT COUNT(*) FROM public.observation WHERE LOWER(record_type) = LOWER('{record_type}')")).scalar()
                print(f"{record_type:<25} | {rec_count:<10} | {obs_count:<15}")
            except Exception as e:
                print(f"{record_type:<25} | Error: {e}")

if __name__ == "__main__":
    check_sync()
