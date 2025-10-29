"""
SQLModel Class Template
---

This module provides a template for creating a new SQLModel class, which
corresponds to a new table in the database.

To use this template:
1.  Copy this file to the `src/models/` directory and give it a descriptive name
    (e.g., `new_data_model.py`).
2.  Rename the class from `ModelTemplate` to your desired model name (e.g., `NewData`).
3.  Update the `__tablename__` to match your desired table name in the database.
4.  Define the fields for your model, replacing the placeholder fields.
5.  Add the new model to `alembic/env.py` by adding a new import line
    (e.g., `from pipeline.models.new_data_model import *`).
"""
from typing import Optional
from sqlmodel import Field, SQLModel


# TODO: Rename 'ModelTemplate' to a descriptive name for your data model.
class ModelTemplate(SQLModel, table=True):
    """
    Represents a template for a new database table.
    """
    # TODO: Set the name of the database table.
    __tablename__ = "model_template_table"

    # --- Fields ---
    # The primary key is typically an auto-incrementing integer.
    id: Optional[int] = Field(default=None, primary_key=True)

    # TODO: Replace the placeholder fields below with the actual fields
    # for your model. Define their types and any constraints.

    # Example of a required text field.
    name: str = Field(index=True)

    # Example of an optional numeric field.
    value: Optional[float] = Field(default=None)

    # Example of a field with a unique constraint.
    unique_identifier: str = Field(unique=True, index=True)
