"""FastAPI application for CA Biositing project.

This module provides the main FastAPI application with REST API endpoints.
"""

from fastapi import FastAPI

app = FastAPI(
    title="CA Biositing API",
    description="REST API for CA Biositing bioeconomy data",
    version="0.1.0"
)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "CA Biositing API", "version": "0.1.0"}


@app.get("/hello")
def read_hello():
    """Hello endpoint."""
    return {"message": "Hello, world"}
