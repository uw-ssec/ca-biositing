from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class LineageGroup(SQLModel, table=True):
    __tablename__ = "lineage_group"

    id: Optional[int] = Field(default=None, primary_key=True)
    etl_run_id: Optional[int] = Field(default=None, foreign_key="etl_run.id")
    note: Optional[str] = Field(default=None)

    # Relationships
    etl_run: Optional["EtlRun"] = Relationship()


class EntityLineage(SQLModel, table=True):
    __tablename__ = "entity_lineage"

    id: Optional[int] = Field(default=None, primary_key=True)
    lineage_group_id: Optional[int] = Field(default=None)
    source_table: Optional[str] = Field(default=None)
    source_row_id: Optional[str] = Field(default=None)
    note: Optional[str] = Field(default=None)

