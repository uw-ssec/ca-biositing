from sqlmodel import Session, select
from ca_biositing.datamodels.database import get_engine
from ca_biositing.datamodels.models.sample_preparation.prepared_sample import PreparedSample
from ca_biositing.datamodels.models.aim1_records import (
    CalorimetryRecord, CompositionalRecord, FtnirRecord, IcpRecord,
    ProximateRecord, RgbRecord, UltimateRecord, XrdRecord, XrfRecord
)
from ca_biositing.datamodels.models.aim2_records import (
    AutoclaveRecord, FermentationRecord, GasificationRecord, PretreatmentRecord
)

def check_orphaned_references():
    import os
    if os.environ.get("POSTGRES_HOST") is None:
        os.environ["POSTGRES_HOST"] = "localhost"

    engine = get_engine()

    analysis_models = [
        CalorimetryRecord, CompositionalRecord, FtnirRecord, IcpRecord,
        ProximateRecord, RgbRecord, UltimateRecord, XrdRecord, XrfRecord,
        AutoclaveRecord, FermentationRecord, GasificationRecord, PretreatmentRecord
    ]

    with Session(engine) as session:
        # Get all valid prepared sample IDs
        valid_prep_ids = set(session.exec(select(PreparedSample.id)).all())

        print(f"Found {len(valid_prep_ids)} valid prepared samples in the database.\n")

        total_orphans = 0
        for model in analysis_models:
            table_name = model.__tablename__
            # Find records where prepared_sample_id is not in valid_prep_ids
            # We filter out None because some records might not have a prepared sample yet
            statement = select(model).where(model.prepared_sample_id != None)
            records = session.exec(statement).all()

            orphans = [r for r in records if r.prepared_sample_id not in valid_prep_ids]

            if orphans:
                print(f"Table: {table_name}")
                print(f"  Found {len(orphans)} records referencing non-existent prepared_sample_id:")
                for o in orphans:
                    print(f"    Record ID: {o.record_id}, Invalid Prepared Sample ID: {o.prepared_sample_id}")
                total_orphans += len(orphans)
            else:
                # print(f"Table: {table_name} - No orphans found.")
                pass

        if total_orphans == 0:
            print("No orphaned references found across all analysis tables.")
        else:
            print(f"\nTotal orphaned references found: {total_orphans}")

if __name__ == "__main__":
    check_orphaned_references()
