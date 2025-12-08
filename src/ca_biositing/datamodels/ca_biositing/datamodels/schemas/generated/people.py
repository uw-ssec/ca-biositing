
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class Contact(Base):
    """
    Contact information for a person.
    """
    __tablename__ = 'Contact'

    id = Column(Integer(), primary_key=True, nullable=False )
    first_name = Column(Text())
    last_name = Column(Text())
    email = Column(Text())
    affiliation = Column(Text())


    def __repr__(self):
        return f"Contact(id={self.id},first_name={self.first_name},last_name={self.last_name},email={self.email},affiliation={self.affiliation},)"






class Provider(Base):
    """
    Provider information.
    """
    __tablename__ = 'Provider'

    id = Column(Integer(), primary_key=True, nullable=False )
    codename = Column(Text())


    def __repr__(self):
        return f"Provider(id={self.id},codename={self.codename},)"
