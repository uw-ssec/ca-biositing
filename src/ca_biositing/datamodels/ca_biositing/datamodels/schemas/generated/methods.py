
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class ParameterCategoryParameter(Base):
    """
    Link between parameter and category.
    """
    __tablename__ = 'ParameterCategoryParameter'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    parameter_category_id = Column(Integer())


    def __repr__(self):
        return f"ParameterCategoryParameter(id={self.id},parameter_id={self.parameter_id},parameter_category_id={self.parameter_category_id},)"






class ParameterUnit(Base):
    """
    Link between parameter and alternate units.
    """
    __tablename__ = 'ParameterUnit'

    id = Column(Integer(), primary_key=True, nullable=False )
    parameter_id = Column(Integer())
    alternate_unit_id = Column(Integer())


    def __repr__(self):
        return f"ParameterUnit(id={self.id},parameter_id={self.parameter_id},alternate_unit_id={self.alternate_unit_id},)"






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






class Unit(LookupBase):
    """
    Unit of measurement.
    """
    __tablename__ = 'Unit'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"Unit(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Method(BaseEntity):
    """
    Analytical method.
    """
    __tablename__ = 'Method'

    name = Column(Text())
    method_abbrev_id = Column(Integer())
    method_category_id = Column(Integer())
    method_standard_id = Column(Integer())
    description = Column(Text())
    detection_limits = Column(Text())
    source_id = Column(Integer())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Method(name={self.name},method_abbrev_id={self.method_abbrev_id},method_category_id={self.method_category_id},method_standard_id={self.method_standard_id},description={self.description},detection_limits={self.detection_limits},source_id={self.source_id},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodAbbrev(LookupBase):
    """
    Abbreviation for a method.
    """
    __tablename__ = 'MethodAbbrev'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodAbbrev(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodCategory(LookupBase):
    """
    Category of a method.
    """
    __tablename__ = 'MethodCategory'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodCategory(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class MethodStandard(LookupBase):
    """
    Standard associated with a method.
    """
    __tablename__ = 'MethodStandard'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"MethodStandard(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class Parameter(BaseEntity):
    """
    Parameter measured.
    """
    __tablename__ = 'Parameter'

    name = Column(Text())
    standard_unit_id = Column(Integer())
    calculated = Column(Boolean())
    description = Column(Text())
    id = Column(Integer(), primary_key=True, nullable=False )
    created_at = Column(DateTime())
    updated_at = Column(DateTime())
    etl_run_id = Column(Text())
    lineage_group_id = Column(Integer())


    def __repr__(self):
        return f"Parameter(name={self.name},standard_unit_id={self.standard_unit_id},calculated={self.calculated},description={self.description},id={self.id},created_at={self.created_at},updated_at={self.updated_at},etl_run_id={self.etl_run_id},lineage_group_id={self.lineage_group_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class ParameterCategory(LookupBase):
    """
    Category of a parameter.
    """
    __tablename__ = 'ParameterCategory'

    id = Column(Integer(), primary_key=True, nullable=False )
    name = Column(Text())
    description = Column(Text())
    uri = Column(Text())


    def __repr__(self):
        return f"ParameterCategory(id={self.id},name={self.name},description={self.description},uri={self.uri},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
