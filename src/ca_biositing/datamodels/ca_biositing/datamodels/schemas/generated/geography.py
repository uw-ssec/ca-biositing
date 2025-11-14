
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


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
