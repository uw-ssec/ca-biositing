"""CA Biositing Data Models Package.

This package contains SQLModel-based database models for the CA Biositing project.
It provides shared data models that can be used across different components of the
application, including ETL pipelines and API services.
"""

from __future__ import annotations

from ca_biositing.datamodels._version import __version__

__all__ = ["__version__"]
