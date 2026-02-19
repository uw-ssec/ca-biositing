from ..base import BaseEntity
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class FileObjectMetadata(BaseEntity, table=True):
    __tablename__ = "file_object_metadata"

    data_source_id: Optional[int] = Field(default=None, foreign_key="data_source.id")
    bucket_path: Optional[str] = Field(default=None)
    file_format: Optional[str] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    checksum_md5: Optional[str] = Field(default=None)
    checksum_sha256: Optional[str] = Field(default=None)

    # Relationships
    data_source: Optional["DataSource"] = Relationship()
