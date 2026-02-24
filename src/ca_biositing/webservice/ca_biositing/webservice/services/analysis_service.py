"""Service layer for feedstock analysis data operations.

This module provides business logic for querying analysis data
(proximate, ultimate, compositional) from the database.
"""

from __future__ import annotations

import re
from typing import Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session, aliased

from ca_biositing.datamodels.models import (
    CompositionalRecord,
    DimensionType,
    FieldSample,
    LocationAddress,
    Observation,
    Parameter,
    Place,
    PreparedSample,
    ProximateRecord,
    Resource,
    UltimateRecord,
    Unit,
)
from ca_biositing.webservice.exceptions import (
    ParameterNotFoundException,
    ResourceNotFoundException,
    ServiceException,
)


class AnalysisService:
    """Business logic for feedstock analysis data operations."""

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
        normalized = AnalysisService._normalize_name(resource_name)
        stmt = select(Resource).where(
            func.lower(func.regexp_replace(Resource.name, r"\s+", " ", "g")) == normalized
        )
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
        # Create alias for the dimension unit join
        DimensionUnit = aliased(Unit)

        # Find all analysis record IDs that match resource + geoid criteria
        # We need to check all three analysis record types
        record_ids = []

        # Query proximate analysis records
        proximate_stmt = (
            select(ProximateRecord.record_id)
            .join(PreparedSample, ProximateRecord.prepared_sample_id == PreparedSample.id)
            .join(FieldSample, PreparedSample.field_sample_id == FieldSample.id)
            .join(LocationAddress, FieldSample.sampling_location_id == LocationAddress.id)
            .where(and_(
                ProximateRecord.resource_id == resource_id,
                LocationAddress.geography_id == geoid
            ))
        )
        proximate_record_ids = session.execute(proximate_stmt).scalars().all()
        record_ids.extend(proximate_record_ids)

        # Query ultimate analysis records
        ultimate_stmt = (
            select(UltimateRecord.record_id)
            .join(PreparedSample, UltimateRecord.prepared_sample_id == PreparedSample.id)
            .join(FieldSample, PreparedSample.field_sample_id == FieldSample.id)
            .join(LocationAddress, FieldSample.sampling_location_id == LocationAddress.id)
            .where(and_(
                UltimateRecord.resource_id == resource_id,
                LocationAddress.geography_id == geoid
            ))
        )
        ultimate_record_ids = session.execute(ultimate_stmt).scalars().all()
        record_ids.extend(ultimate_record_ids)

        # Query compositional analysis records
        compositional_stmt = (
            select(CompositionalRecord.record_id)
            .join(PreparedSample, CompositionalRecord.prepared_sample_id == PreparedSample.id)
            .join(FieldSample, PreparedSample.field_sample_id == FieldSample.id)
            .join(LocationAddress, FieldSample.sampling_location_id == LocationAddress.id)
            .where(and_(
                CompositionalRecord.resource_id == resource_id,
                LocationAddress.geography_id == geoid
            ))
        )
        compositional_record_ids = session.execute(compositional_stmt).scalars().all()
        record_ids.extend(compositional_record_ids)

        # If no matching records found, return empty list
        if not record_ids:
            return []

        # Query observations using the matching record_ids
        stmt = (
            select(
                Observation,
                Parameter.name.label("parameter_name"),
                Unit.name.label("unit_name"),
                DimensionType.name.label("dimension_name"),
                DimensionUnit.name.label("dimension_unit_name"),
            )
            .join(Parameter, Observation.parameter_id == Parameter.id)
            .join(Unit, Observation.unit_id == Unit.id)
            .outerjoin(DimensionType, Observation.dimension_type_id == DimensionType.id)
            .outerjoin(DimensionUnit, Observation.dimension_unit_id == DimensionUnit.id)
            .where(and_(
                Observation.record_id.in_(record_ids),
                or_(
                    Observation.record_type == "proximate analysis",
                    Observation.record_type == "ultimate analysis",
                    Observation.record_type == "compositional analysis"
                )
            ))
        )

        if parameter_name:
            stmt = stmt.where(Parameter.name == parameter_name)

        # Order by observation ID for deterministic results
        stmt = stmt.order_by(Observation.id)

        results = session.execute(stmt).all()

        observations = []
        for row in results:
            obs = row.Observation
            observations.append({
                "parameter": row.parameter_name,
                "value": float(obs.value) if obs.value is not None else None,
                "unit": row.unit_name,
                "dimension": row.dimension_name,
                "dimension_value": float(obs.dimension_value) if obs.dimension_value is not None else None,
                "dimension_unit": row.dimension_unit_name,
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
