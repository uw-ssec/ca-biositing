from ..base import LookupBase
from sqlmodel import SQLModel


class LocationResolution(LookupBase, table=True):
    __tablename__ = "location_resolution"
