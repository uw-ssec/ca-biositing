"""Service layer for feedstock analysis data operations.

This module provides business logic for querying analysis data
(proximate, ultimate, compositional) from the database.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ca_biositing.datamodels.models import Resource
from ca_biositing.webservice.exceptions import (
    ParameterNotFoundException,
    ResourceNotFoundException,
)
from ca_biositing.webservice.services._canonical_views import get_analysis_data_view


class AnalysisService:
    """Business logic for feedstock analysis data operations."""

    @staticmethod
    def _get_resource_by_name(session: Session, resource_name: str) -> Resource:
        """Get resource by name.

        Args:
            session: Database session
            resource_name: Resource name

        Returns:
            Resource object

        Raises:
            ResourceNotFoundException: If resource not found
        """
        stmt = select(Resource).where(Resource.name == resource_name)
        resource = session.execute(stmt).scalar_one_or_none()

        if not resource:
            raise ResourceNotFoundException(resource_name)

        return resource

    @staticmethod
    def _get_observations_for_analysis(
        session: Session,
        resource_id: int,
        geoid: str,
        parameter_name: Optional[str] = None
    ) -> list[dict]:
        """Get observations for analysis records by resource and geoid.

        Queries all analysis types (proximate, ultimate, compositional) that match
        the resource and geoid criteria through the chain:
        AnalysisRecord -> PreparedSample -> FieldSample -> LocationAddress -> Place

        Args:
            session: Database session
            resource_id: Resource ID
            geoid: Geographic identifier
            parameter_name: Optional parameter name filter

        Returns:
            List of observation dictionaries with parameter/unit/dimension details
        """
        analysis_view = get_analysis_data_view(session)
        stmt = (
            select(
                analysis_view.c.id,
                analysis_view.c.parameter,
                analysis_view.c.value,
                analysis_view.c.unit,
                analysis_view.c.dimension,
                analysis_view.c.dimension_value,
                analysis_view.c.dimension_unit,
            )
            .where(and_(
                analysis_view.c.resource_id == resource_id,
                analysis_view.c.geoid == geoid,
            ))
        )

        if parameter_name:
            stmt = stmt.where(analysis_view.c.parameter == parameter_name)

        # Order by observation ID for deterministic results
        stmt = stmt.order_by(analysis_view.c.id)

        results = session.execute(stmt).all()

        observations = []
        for row in results:
            observations.append({
                "parameter": row.parameter,
                "value": float(row.value) if row.value is not None else None,
                "unit": row.unit,
                "dimension": row.dimension,
                "dimension_value": float(row.dimension_value)
                if row.dimension_value is not None else None,
                "dimension_unit": row.dimension_unit,
            })

        return observations

    @staticmethod
    def get_by_resource(
        session: Session,
        resource: str,
        geoid: str,
        parameter: str
    ) -> dict:
        """Get single analysis parameter by resource name.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier
            parameter: Parameter name

        Returns:
            Dictionary with analysis data

        Raises:
            ResourceNotFoundException: If resource not found
            ParameterNotFoundException: If parameter not found for resource/geoid
        """
        # Validate resource exists
        resource_obj = AnalysisService._get_resource_by_name(session, resource)

        # Get observations for this resource
        observations = AnalysisService._get_observations_for_analysis(
            session,
            resource_obj.id,
            geoid,
            parameter_name=parameter
        )

        if not observations:
            raise ParameterNotFoundException(parameter, f"resource {resource} in geoid {geoid}")

        # Return first matching observation
        obs = observations[0]
        return {
            "resource": resource,
            "geoid": geoid,
            "parameter": obs["parameter"],
            "value": obs["value"],
            "unit": obs["unit"],
        }

    @staticmethod
    def list_by_resource(
        session: Session,
        resource: str,
        geoid: str
    ) -> dict:
        """List all analysis parameters for a resource.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier

        Returns:
            Dictionary with resource, geoid, and list of parameters

        Raises:
            ResourceNotFoundException: If resource not found
        """
        # Validate resource exists
        resource_obj = AnalysisService._get_resource_by_name(session, resource)

        # Get all observations for this resource
        observations = AnalysisService._get_observations_for_analysis(
            session,
            resource_obj.id,
            geoid
        )

        # Format as list of parameter data
        data_items = [
            {
                "parameter": obs["parameter"],
                "value": obs["value"],
                "unit": obs["unit"],
                "dimension": obs["dimension"],
                "dimension_value": obs["dimension_value"],
                "dimension_unit": obs["dimension_unit"],
            }
            for obs in observations
        ]

        return {
            "resource": resource,
            "geoid": geoid,
            "data": data_items,
        }
