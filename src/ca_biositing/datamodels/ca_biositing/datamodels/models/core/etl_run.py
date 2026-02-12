from datetime import datetime
from sqlmodel import Field, SQLModel
from typing import Optional


class EtlRun(SQLModel, table=True):
    __tablename__ = "etl_run"

    id: Optional[int] = Field(default=None, primary_key=True)
    run_id: Optional[str] = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    pipeline_name: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    records_ingested: Optional[int] = Field(default=None)
    note: Optional[str] = Field(default=None)

