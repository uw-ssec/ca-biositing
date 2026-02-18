from ca_biositing.pipeline.utils.engine import engine
from sqlalchemy import text

def check_db():
    with engine.connect() as conn:
        print('FileObjectMetadata count:', conn.execute(text('SELECT count(*) FROM file_object_metadata')).scalar())
        print('ICP records with raw_data_id:', conn.execute(text('SELECT count(*) FROM icp_record WHERE raw_data_id IS NOT NULL')).scalar())
        print('XRD records with raw_data_id:', conn.execute(text('SELECT count(*) FROM xrd_record WHERE raw_data_id IS NOT NULL')).scalar())
        print('XRF records with raw_data_id:', conn.execute(text('SELECT count(*) FROM xrf_record WHERE raw_data_id IS NOT NULL')).scalar())
        print('Proximate records with raw_data_id:', conn.execute(text('SELECT count(*) FROM proximate_record WHERE raw_data_id IS NOT NULL')).scalar())

        rows = conn.execute(text('SELECT id, uri FROM file_object_metadata')).all()
        print('Sample FileObjectMetadata rows:', rows)

if __name__ == "__main__":
    check_db()
