"""Custom exception classes for CA Biositing API.

This module defines custom HTTP exceptions used across all API endpoints
to provide consistent error responses to clients.
"""

from __future__ import annotations

from fastapi import HTTPException, status


class CropNotFoundException(HTTPException):
    """Raised when usda_crop is not found in the database.

    This exception is raised when a client requests data for a crop
    that does not exist in the usda_commodity table.
    """

    def __init__(self, crop: str):
        """Initialize the exception with the crop name.

        Args:
            crop: The crop name that was not found
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Crop not found: {crop}",
        )


class ResourceNotFoundException(HTTPException):
    """Raised when resource is not found in the database.

    This exception is raised when a client requests data for a resource
    that does not exist in the primary_ag_product table.
    """

    def __init__(self, resource: str):
        """Initialize the exception with the resource name.

        Args:
            resource: The resource name that was not found
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource not found: {resource}",
        )


class ParameterNotFoundException(HTTPException):
    """Raised when parameter is not found for a given crop/resource.

    This exception is raised when a client requests a specific parameter
    that does not exist in the data for the given crop, resource, or geoid.
    """

    def __init__(self, parameter: str, identifier: str):
        """Initialize the exception with parameter and identifier.

        Args:
            parameter: The parameter name that was not found
            identifier: The crop, resource, or geoid context (e.g., "crop CORN in geoid 06001")
        """
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parameter '{parameter}' not found for {identifier}",
        )


class ParameterErrorException(HTTPException):
    """Raised for invalid parameter combinations or values.

    This exception is raised when:
    - Both usda_crop and resource are specified (mutually exclusive)
    - Neither usda_crop nor resource are specified
    - Invalid parameter combinations
    - Invalid parameter values that don't pass business logic validation
    """

    def __init__(self, message: str):
        """Initialize the exception with a custom message.

        Args:
            message: Description of the parameter error
        """
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
        )


class ServiceException(HTTPException):
    """Raised for generic server errors.

    This exception is raised for internal service errors such as:
    - Database connection failures
    - External service timeouts
    - Unexpected server-side errors
    """

    def __init__(self, message: str = "Internal service error occurred"):
        """Initialize the exception with a custom message.

        Args:
            message: Description of the service error
        """
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
