"""Service layer for resource availability data operations.

This module provides business logic for querying resource availability
(from_month, to_month) from the database.
"""

from __future__ import annotations

import re

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from ca_biositing.datamodels.models import (
    Resource,
    ResourceAvailability,
)
from ca_biositing.webservice.exceptions import (
    ResourceNotFoundException,
)


class AvailabilityService:
    """Business logic for resource availability data operations."""

    @staticmethod
    def _normalize_name(name: str) -> str:
        """Normalize a name for case- and whitespace-insensitive lookup."""
        return re.sub(r"\s+", " ", name).strip().lower()

    @staticmethod
    def _get_resource_by_name(session: Session, resource_name: str) -> Resource:
        """Get resource by name (case/whitespace insensitive).

        Args:
            session: Database session
            resource_name: Resource name

        Returns:
            Resource object

        Raises:
            ResourceNotFoundException: If resource not found
        """
        normalized = AvailabilityService._normalize_name(resource_name)
        stmt = select(Resource).where(
            func.lower(func.regexp_replace(Resource.name, r"\s+", " ", "g")) == normalized
        )
        resource = session.execute(stmt).scalar_one_or_none()

        if not resource:
            raise ResourceNotFoundException(resource_name)

        return resource

    @staticmethod
    def get_by_resource(
        session: Session,
        resource: str,
        geoid: str
    ) -> dict:
        """Get availability data by resource name and geoid.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier

        Returns:
            Dictionary with resource, geoid, from_month, to_month

        Raises:
            ResourceNotFoundException: If resource not found or no availability data
        """
        # Validate resource exists
        resource_obj = AvailabilityService._get_resource_by_name(session, resource)

        # Query resource availability
        stmt = (
            select(ResourceAvailability)
            .where(and_(
                ResourceAvailability.resource_id == resource_obj.id,
                ResourceAvailability.geoid == geoid
            ))
        )
        availability = session.execute(stmt).scalar_one_or_none()

        if not availability:
            raise ResourceNotFoundException(
                f"{resource} (no availability data for geoid {geoid})"
            )

        return {
            "resource": resource,
            "geoid": geoid,
            "from_month": availability.from_month,
            "to_month": availability.to_month,
        }
