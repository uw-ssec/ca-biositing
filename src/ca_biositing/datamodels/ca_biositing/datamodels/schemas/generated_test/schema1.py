
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata


class ClassA(Base):
    """

    """
    __tablename__ = 'class_a'

    id = Column(Text(), primary_key=True, nullable=False )


    def __repr__(self):
        return f"ClassA(id={self.id},)"
