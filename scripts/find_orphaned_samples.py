from sqlmodel import Session, select
import os
from ca_biositing.datamodels.database import get_engine
from ca_biositing.datamodels.models.sample_preparation.prepared_sample import PreparedSample
from ca_biositing.datamodels.models.aim1_records import (
    CalorimetryRecord, CompositionalRecord, FtnirRecord, IcpRecord,
    ProximateRecord, RgbRecord, UltimateRecord, XrdRecord, XrfRecord
)
from ca_biositing.datamodels.models.aim2_records import (
    AutoclaveRecord, FermentationRecord, GasificationRecord, PretreatmentRecord
)

def find_orphaned_prepared_samples():
    if os.environ.get("POSTGRES_HOST") is None:
        os.environ["POSTGRES_HOST"] = "localhost"

    engine = get_engine()

    analysis_models = [
        CalorimetryRecord, CompositionalRecord, FtnirRecord, IcpRecord,
        ProximateRecord, RgbRecord, UltimateRecord, XrdRecord, XrfRecord,
        AutoclaveRecord, FermentationRecord, GasificationRecord, PretreatmentRecord
    ]

    with Session(engine) as session:
        # 1. Find PreparedSamples with no FieldSample linked
        statement = select(PreparedSample).where(PreparedSample.field_sample_id == None)
        orphaned_preps = session.exec(statement).all()

        if not orphaned_preps:
            print("No prepared samples found with missing field_sample_id.")
            return

        print(f"Found {len(orphaned_preps)} prepared samples with no linked field sample.\n")

        orphan_ids = [p.id for p in orphaned_preps]
        orphan_map = {p.id: p for p in orphaned_preps}

        # 2. Track which analysis records reference these orphans
        print("References in analysis tables:")
        total_references = 0

        for model in analysis_models:
            table_name = model.__tablename__
            statement = select(model).where(model.prepared_sample_id.in_(orphan_ids))
            records = session.exec(statement).all()

            if records:
                print(f"\nTable: {table_name}")
                for r in records:
                    prep = orphan_map[r.prepared_sample_id]
                    print(f"  - Record: {r.record_id} -> Prepared Sample: '{prep.name}' (ID: {prep.id})")
                total_references += len(records)

        if total_references == 0:
            print("\nNone of these orphaned prepared samples are currently referenced by analysis records.")
        else:
            print(f"\nTotal references found: {total_references}")

if __name__ == "__main__":
    find_orphaned_prepared_samples()
