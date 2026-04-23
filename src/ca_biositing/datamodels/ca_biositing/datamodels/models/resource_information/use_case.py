from ..base import LookupBase


class UseCase(LookupBase, table=True):
    __tablename__ = "use_case"
