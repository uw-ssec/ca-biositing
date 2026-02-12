from datetime import datetime, timezone
from typing import Optional
from prefect import task, get_run_logger
from prefect.context import FlowRunContext
from sqlalchemy.orm import Session
from ca_biositing.pipeline.utils.engine import engine

@task
def create_etl_run_record(pipeline_name: str) -> str:
    """
    Creates an EtlRun record in the database using the Prefect run_id.
    """
    from ca_biositing.datamodels.models import EtlRun

    ctx = FlowRunContext.get()
    if not ctx:
        raise RuntimeError("create_etl_run_record must be called within a flow or task context.")

    run_id_str = str(ctx.flow_run.id)
    logger = get_run_logger()

    with Session(engine) as session:
        # Check if it already exists by run_id
        existing = session.query(EtlRun).filter(EtlRun.run_id == run_id_str).first()
        if existing:
            return str(existing.id)

        etl_run = EtlRun(
            run_id=run_id_str,
            started_at=datetime.now(timezone.utc),
            pipeline_name=pipeline_name,
            status="RUNNING"
        )
        session.add(etl_run)
        session.commit()
        session.refresh(etl_run)
        logger.info(f"Created EtlRun record: {etl_run.id} for Prefect run {run_id_str}")

        return str(etl_run.id)

@task
def create_lineage_group(etl_run_id: str, note: Optional[str] = None) -> int:
    """
    Creates a LineageGroup record associated with an EtlRun.
    Returns the integer ID of the new lineage group.
    """
    from ca_biositing.datamodels.models import LineageGroup

    logger = get_run_logger()

    with Session(engine) as session:
        lineage_group = LineageGroup(
            etl_run_id=etl_run_id,
            note=note
        )
        session.add(lineage_group)
        session.commit()
        session.refresh(lineage_group)
        logger.info(f"Created LineageGroup record: {lineage_group.id}")
        return lineage_group.id
