
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class USDARecord(Base):
    """
    Base class for USDA agricultural data records.
    """
    __tablename__ = 'USDARecord'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    year = Column(Integer(), nullable=False )
    crop = Column(Enum('Almond', 'Pistachio', 'Tomato', 'Olive', name='CropEnum'))
    variable = Column(Enum('ACREAGE_TOTAL', 'ACREAGE_BEARING', 'ACREAGE_NONBEARING', 'YIELD', 'PRODUCTION', 'OPERATIONS', name='VariableEnum'))
    unit = Column(Enum('ACRES', 'TONS', 'TONS_PER_ACRE', 'OPERATIONS', name='UnitEnum'))
    value = Column(Float())
    bearing_status = Column(Enum('BEARING', 'NONBEARING', 'NA', name='BearingStatusEnum'))
    class_desc = Column(Text())
    domain_desc = Column(Text())
    source = Column(Text())
    notes = Column(Text())
    geography_id = Column(Integer(), ForeignKey('Geography.id'))
    geography = relationship("Geography", uselist=False, foreign_keys=[geography_id])


    def __repr__(self):
        return f"USDARecord(id={self.id},year={self.year},crop={self.crop},variable={self.variable},unit={self.unit},value={self.value},bearing_status={self.bearing_status},class_desc={self.class_desc},domain_desc={self.domain_desc},source={self.source},notes={self.notes},geography_id={self.geography_id},)"






class Geography(Base):
    """
    Reference table for U.S. geographic identifiers.
    """
    __tablename__ = 'Geography'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    state_name = Column(Text())
    state_fips = Column(Text())
    county_name = Column(Text())
    county_fips = Column(Text())
    geoid = Column(Text())
    region_name = Column(Text())
    agg_level_desc = Column(Text())


    def __repr__(self):
        return f"Geography(id={self.id},state_name={self.state_name},state_fips={self.state_fips},county_name={self.county_name},county_fips={self.county_fips},geoid={self.geoid},region_name={self.region_name},agg_level_desc={self.agg_level_desc},)"






class CensusRecord(USDARecord):
    """
    A USDA Census of Agriculture record (every 5 years).
    """
    __tablename__ = 'CensusRecord'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    year = Column(Integer(), nullable=False )
    crop = Column(Enum('Almond', 'Pistachio', 'Tomato', 'Olive', name='CropEnum'))
    variable = Column(Enum('ACREAGE_TOTAL', 'ACREAGE_BEARING', 'ACREAGE_NONBEARING', 'YIELD', 'PRODUCTION', 'OPERATIONS', name='VariableEnum'))
    unit = Column(Enum('ACRES', 'TONS', 'TONS_PER_ACRE', 'OPERATIONS', name='UnitEnum'))
    value = Column(Float())
    bearing_status = Column(Enum('BEARING', 'NONBEARING', 'NA', name='BearingStatusEnum'))
    class_desc = Column(Text())
    domain_desc = Column(Text())
    source = Column(Text())
    notes = Column(Text())
    geography_id = Column(Integer(), ForeignKey('Geography.id'))
    geography = relationship("Geography", uselist=False, foreign_keys=[geography_id])


    def __repr__(self):
        return f"CensusRecord(id={self.id},year={self.year},crop={self.crop},variable={self.variable},unit={self.unit},value={self.value},bearing_status={self.bearing_status},class_desc={self.class_desc},domain_desc={self.domain_desc},source={self.source},notes={self.notes},geography_id={self.geography_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }



class SurveyRecord(USDARecord):
    """
    A USDA Survey record (annual, seasonal, or periodic).
    """
    __tablename__ = 'SurveyRecord'

    id = Column(Integer(), primary_key=True, autoincrement=True , nullable=False )
    period_desc = Column(Text())
    freq_desc = Column(Text())
    program_desc = Column(Text())
    year = Column(Integer(), nullable=False )
    crop = Column(Enum('Almond', 'Pistachio', 'Tomato', 'Olive', name='CropEnum'))
    variable = Column(Enum('ACREAGE_TOTAL', 'ACREAGE_BEARING', 'ACREAGE_NONBEARING', 'YIELD', 'PRODUCTION', 'OPERATIONS', name='VariableEnum'))
    unit = Column(Enum('ACRES', 'TONS', 'TONS_PER_ACRE', 'OPERATIONS', name='UnitEnum'))
    value = Column(Float())
    bearing_status = Column(Enum('BEARING', 'NONBEARING', 'NA', name='BearingStatusEnum'))
    class_desc = Column(Text())
    domain_desc = Column(Text())
    source = Column(Text())
    notes = Column(Text())
    geography_id = Column(Integer(), ForeignKey('Geography.id'))
    geography = relationship("Geography", uselist=False, foreign_keys=[geography_id])


    def __repr__(self):
        return f"SurveyRecord(id={self.id},period_desc={self.period_desc},freq_desc={self.freq_desc},program_desc={self.program_desc},year={self.year},crop={self.crop},variable={self.variable},unit={self.unit},value={self.value},bearing_status={self.bearing_status},class_desc={self.class_desc},domain_desc={self.domain_desc},source={self.source},notes={self.notes},geography_id={self.geography_id},)"




    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
