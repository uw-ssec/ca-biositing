
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class LineageGroup(Base):
    """
    Grouping for lineage information.
    """
    __tablename__ = 'LineageGroup'

    id = Column(Integer(), primary_key=True, nullable=False )
    etl_run_id = Column(Text())
    note = Column(Text())


    def __repr__(self):
        return f"LineageGroup(id={self.id},etl_run_id={self.etl_run_id},note={self.note},)"






class EntityLineage(Base):
    """
    Lineage information for a specific entity.
    """
    __tablename__ = 'EntityLineage'

    id = Column(Integer(), primary_key=True, nullable=False )
    lineage_group_id = Column(Integer())
    source_table = Column(Text())
    source_row_id = Column(Text())
    note = Column(Text())


    def __repr__(self):
        return f"EntityLineage(id={self.id},lineage_group_id={self.lineage_group_id},source_table={self.source_table},source_row_id={self.source_row_id},note={self.note},)"






class EtlRun(Base):
    """
    Information about an ETL run.
    """
    __tablename__ = 'EtlRun'

    id = Column(Integer(), primary_key=True, nullable=False )
    started_at = Column(DateTime())
    completed_at = Column(DateTime())
    pipeline_name = Column(Text())
    status = Column(Text())
    records_ingested = Column(Integer())
    note = Column(Text())


    def __repr__(self):
        return f"EtlRun(id={self.id},started_at={self.started_at},completed_at={self.completed_at},pipeline_name={self.pipeline_name},status={self.status},records_ingested={self.records_ingested},note={self.note},)"






class BaseEntity(Base):
    """
    Base entity included in all main entity tables.
    """
    __tablename__ = 'BaseEntity'

    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"BaseEntity(id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"






class LookupBase(Base):
    """
    Base class for enum/ontology-like tables.
    """
    __tablename__ = 'LookupBase'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"LookupBase(id={self.id},name={self.name},description={self.description},uri={self.uri},)"
