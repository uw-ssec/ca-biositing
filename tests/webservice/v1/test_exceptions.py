"""Tests for custom API exceptions.

This module tests that all custom exceptions are properly initialized
with the correct HTTP status codes and error messages.
"""

from __future__ import annotations

import pytest
from fastapi import status

from ca_biositing.webservice.exceptions import (
    CropNotFoundException,
    ParameterErrorException,
    ParameterNotFoundException,
    ResourceNotFoundException,
    ServiceException,
)


class TestCropNotFoundException:
    """Test cases for CropNotFoundException."""

    def test_exception_status_code(self):
        """Test that exception has correct HTTP status code."""
        exc = CropNotFoundException("CORN")
        assert exc.status_code == status.HTTP_404_NOT_FOUND

    def test_exception_detail_message(self):
        """Test that exception contains crop name in detail message."""
        crop_name = "SOYBEANS"
        exc = CropNotFoundException(crop_name)
        assert crop_name in exc.detail
        assert "not found" in exc.detail.lower()

    def test_exception_with_special_characters(self):
        """Test exception handles crop names with special characters."""
        crop_name = "CORN, GRAIN"
        exc = CropNotFoundException(crop_name)
        assert crop_name in exc.detail


class TestResourceNotFoundException:
    """Test cases for ResourceNotFoundException."""

    def test_exception_status_code(self):
        """Test that exception has correct HTTP status code."""
        exc = ResourceNotFoundException("corn_grain")
        assert exc.status_code == status.HTTP_404_NOT_FOUND

    def test_exception_detail_message(self):
        """Test that exception contains resource name in detail message."""
        resource_name = "soybean_meal"
        exc = ResourceNotFoundException(resource_name)
        assert resource_name in exc.detail
        assert "not found" in exc.detail.lower()

    def test_exception_with_underscores(self):
        """Test exception handles resource names with underscores."""
        resource_name = "corn_stover_grain"
        exc = ResourceNotFoundException(resource_name)
        assert resource_name in exc.detail


class TestParameterNotFoundException:
    """Test cases for ParameterNotFoundException."""

    def test_exception_status_code(self):
        """Test that exception has correct HTTP status code."""
        exc = ParameterNotFoundException("acres", "crop CORN")
        assert exc.status_code == status.HTTP_404_NOT_FOUND

    def test_exception_detail_message_with_parameter(self):
        """Test that exception contains parameter name in detail message."""
        parameter = "yield_per_acre"
        identifier = "crop CORN in geoid 06001"
        exc = ParameterNotFoundException(parameter, identifier)
        assert parameter in exc.detail
        assert identifier in exc.detail
        assert "not found" in exc.detail.lower()

    def test_exception_with_complex_identifier(self):
        """Test exception with complex identifier string."""
        parameter = "production"
        identifier = "resource corn_grain in geoid 06001 for year 2022"
        exc = ParameterNotFoundException(parameter, identifier)
        assert parameter in exc.detail
        assert identifier in exc.detail


class TestParameterErrorException:
    """Test cases for ParameterErrorException."""

    def test_exception_status_code(self):
        """Test that exception has correct HTTP status code."""
        exc = ParameterErrorException("Test error message")
        assert exc.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_exception_custom_message(self):
        """Test that exception uses custom error message."""
        custom_message = "Cannot specify both usda_crop and resource"
        exc = ParameterErrorException(custom_message)
        assert exc.detail == custom_message

    def test_exception_missing_parameter_message(self):
        """Test exception for missing required parameters."""
        message = "Must specify either usda_crop or resource"
        exc = ParameterErrorException(message)
        assert exc.detail == message

    def test_exception_invalid_combination_message(self):
        """Test exception for invalid parameter combinations."""
        message = "Invalid parameter combination: crop and resource are mutually exclusive"
        exc = ParameterErrorException(message)
        assert exc.detail == message


class TestServiceException:
    """Test cases for ServiceException."""

    def test_exception_status_code(self):
        """Test that exception has correct HTTP status code."""
        exc = ServiceException()
        assert exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_exception_default_message(self):
        """Test that exception has default error message."""
        exc = ServiceException()
        assert "internal service error" in exc.detail.lower()

    def test_exception_custom_message(self):
        """Test that exception accepts custom error message."""
        custom_message = "Database connection failed"
        exc = ServiceException(custom_message)
        assert exc.detail == custom_message

    def test_exception_database_error_message(self):
        """Test exception for database errors."""
        message = "Failed to connect to database: connection timeout"
        exc = ServiceException(message)
        assert exc.detail == message

    def test_exception_external_service_error(self):
        """Test exception for external service failures."""
        message = "External API request failed: timeout after 30s"
        exc = ServiceException(message)
        assert exc.detail == message


class TestExceptionInheritance:
    """Test that all exceptions properly inherit from HTTPException."""

    def test_crop_not_found_is_http_exception(self):
        """Test CropNotFoundException inherits from HTTPException."""
        from fastapi import HTTPException

        exc = CropNotFoundException("CORN")
        assert isinstance(exc, HTTPException)

    def test_resource_not_found_is_http_exception(self):
        """Test ResourceNotFoundException inherits from HTTPException."""
        from fastapi import HTTPException

        exc = ResourceNotFoundException("corn_grain")
        assert isinstance(exc, HTTPException)

    def test_parameter_not_found_is_http_exception(self):
        """Test ParameterNotFoundException inherits from HTTPException."""
        from fastapi import HTTPException

        exc = ParameterNotFoundException("acres", "crop CORN")
        assert isinstance(exc, HTTPException)

    def test_parameter_error_is_http_exception(self):
        """Test ParameterErrorException inherits from HTTPException."""
        from fastapi import HTTPException

        exc = ParameterErrorException("Error message")
        assert isinstance(exc, HTTPException)

    def test_service_exception_is_http_exception(self):
        """Test ServiceException inherits from HTTPException."""
        from fastapi import HTTPException

        exc = ServiceException()
        assert isinstance(exc, HTTPException)
