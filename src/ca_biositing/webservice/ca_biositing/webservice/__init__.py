"""CA Biositing API Package.

This package contains the FastAPI application for the CA Biositing project.
It provides REST API endpoints for accessing bioeconomy data.
"""

from __future__ import annotations

from importlib.metadata import version

__version__ = version("ca-biositing-webservice")

__all__ = ["__version__"]
