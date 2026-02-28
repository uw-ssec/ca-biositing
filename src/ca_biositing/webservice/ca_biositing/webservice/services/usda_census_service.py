"""Service layer for USDA Census data operations.

This module provides business logic for querying USDA census data
from the database, including data validation and transformation.
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ca_biositing.datamodels.models import (
    Resource,
    ResourceUsdaCommodityMap,
    UsdaCommodity,
)
from ca_biositing.webservice.exceptions import (
    ParameterNotFoundException,
    ResourceNotFoundException,
)
from ca_biositing.webservice.services._canonical_views import get_usda_census_view
from ca_biositing.webservice.services._usda_lookup_common import get_commodity_by_name


class UsdaCensusService:
    """Business logic for USDA Census data operations."""

    @staticmethod
    def _get_commodity_by_name(session: Session, crop_name: str) -> UsdaCommodity:
        """Get USDA commodity by crop name.

        Args:
            session: Database session
            crop_name: USDA crop name

        Returns:
            UsdaCommodity object

        Raises:
            CropNotFoundException: If crop not found
        """
        return get_commodity_by_name(session, crop_name)

    @staticmethod
    def _get_commodity_by_resource(session: Session, resource_name: str) -> UsdaCommodity:
        """Get USDA commodity by resource name via mapping table.

        Args:
            session: Database session
            resource_name: Resource name

        Returns:
            UsdaCommodity object

        Raises:
            ResourceNotFoundException: If resource not found or no mapping exists
        """

        # First find the resource
        stmt = select(Resource).where(Resource.name == resource_name)
        resource = session.execute(stmt).scalar_one_or_none()

        if not resource:
            raise ResourceNotFoundException(resource_name)

        # Find the commodity mapping
        stmt = (
            select(UsdaCommodity)
            .join(ResourceUsdaCommodityMap, ResourceUsdaCommodityMap.usda_commodity_id == UsdaCommodity.id)
            .where(ResourceUsdaCommodityMap.resource_id == resource.id)
        )
        commodity = session.execute(stmt).scalar_one_or_none()

        if not commodity:
            raise ResourceNotFoundException(
                f"{resource_name} (no USDA commodity mapping found)"
            )

        return commodity

    @staticmethod
    def _get_observations_for_census_record(
        session: Session,
        commodity_id: int,
        geoid: str,
        parameter_name: Optional[str] = None
    ) -> list[dict]:
        """Get observations for a census record by commodity and geoid.

        Since observations are stored separately with unique record_ids,
        we query them by matching dataset + commodity + geoid criteria.

        Args:
            session: Database session
            commodity_id: USDA commodity ID
            geoid: Geographic identifier
            parameter_name: Optional parameter name filter

        Returns:
            List of observation dictionaries with parameter/unit/dimension details
        """
        census_view = get_usda_census_view(session)

        latest_record_stmt = (
            select(census_view.c.source_record_id)
            .where(and_(
                census_view.c.commodity_id == commodity_id,
                census_view.c.geoid == geoid,
            ))
            .order_by(
                census_view.c.record_year.desc(),
                census_view.c.source_record_id.desc(),
            )
            .limit(1)
        )
        latest_record_id = session.execute(latest_record_stmt).scalar_one_or_none()

        if latest_record_id is None:
            return []

        stmt = (
            select(
                census_view.c.id,
                census_view.c.parameter,
                census_view.c.value,
                census_view.c.unit,
                census_view.c.dimension,
                census_view.c.dimension_value,
                census_view.c.dimension_unit,
            )
            .where(and_(
                census_view.c.commodity_id == commodity_id,
                census_view.c.geoid == geoid,
                census_view.c.source_record_id == latest_record_id,
            ))
        )

        if parameter_name:
            stmt = stmt.where(census_view.c.parameter == parameter_name)

        # Order by observation ID for deterministic results
        stmt = stmt.order_by(census_view.c.id)

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
    def get_by_crop(
        session: Session,
        usda_crop: str,
        geoid: str,
        parameter: str
    ) -> dict:
        """Get single census parameter by crop name.

        Args:
            session: Database session
            usda_crop: USDA crop name
            geoid: Geographic identifier
            parameter: Parameter name

        Returns:
            Dictionary with census data

        Raises:
            CropNotFoundException: If crop not found
            ParameterNotFoundException: If parameter not found for crop/geoid
        """
        # Validate crop exists
        commodity = UsdaCensusService._get_commodity_by_name(session, usda_crop)

        # Get observations
        observations = UsdaCensusService._get_observations_for_census_record(
            session, commodity.id, geoid, parameter
        )

        if not observations:
            raise ParameterNotFoundException(
                parameter,
                f"crop {usda_crop} in geoid {geoid}"
            )

        # Return first observation with metadata
        obs = observations[0]
        return {
            "usda_crop": usda_crop,
            "resource": None,
            "geoid": geoid,
            "parameter": obs["parameter"],
            "value": obs["value"],
            "unit": obs["unit"],
            "dimension": obs["dimension"],
            "dimension_value": obs["dimension_value"],
            "dimension_unit": obs["dimension_unit"],
        }

    @staticmethod
    def get_by_resource(
        session: Session,
        resource: str,
        geoid: str,
        parameter: str
    ) -> dict:
        """Get single census parameter by resource name.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier
            parameter: Parameter name

        Returns:
            Dictionary with census data

        Raises:
            ResourceNotFoundException: If resource not found
            ParameterNotFoundException: If parameter not found for resource/geoid
        """
        # Convert resource to commodity
        commodity = UsdaCensusService._get_commodity_by_resource(session, resource)

        # Get observations
        observations = UsdaCensusService._get_observations_for_census_record(
            session, commodity.id, geoid, parameter
        )

        if not observations:
            raise ParameterNotFoundException(
                parameter,
                f"resource {resource} in geoid {geoid}"
            )

        # Return first observation with metadata
        obs = observations[0]
        return {
            "usda_crop": None,
            "resource": resource,
            "geoid": geoid,
            "parameter": obs["parameter"],
            "value": obs["value"],
            "unit": obs["unit"],
            "dimension": obs["dimension"],
            "dimension_value": obs["dimension_value"],
            "dimension_unit": obs["dimension_unit"],
        }

    @staticmethod
    def list_by_crop(
        session: Session,
        usda_crop: str,
        geoid: str
    ) -> dict:
        """List all census parameters for crop/geoid.

        Args:
            session: Database session
            usda_crop: USDA crop name
            geoid: Geographic identifier

        Returns:
            Dictionary with list of all parameters

        Raises:
            CropNotFoundException: If crop not found
            ParameterNotFoundException: If no data found for crop/geoid
        """
        # Validate crop exists
        commodity = UsdaCensusService._get_commodity_by_name(session, usda_crop)

        # Get all observations
        observations = UsdaCensusService._get_observations_for_census_record(
            session, commodity.id, geoid
        )

        if not observations:
            raise ParameterNotFoundException(
                "any parameter",
                f"crop {usda_crop} in geoid {geoid}"
            )

        return {
            "usda_crop": usda_crop,
            "resource": None,
            "geoid": geoid,
            "data": observations,
        }

    @staticmethod
    def list_by_resource(
        session: Session,
        resource: str,
        geoid: str
    ) -> dict:
        """List all census parameters for resource/geoid.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier

        Returns:
            Dictionary with list of all parameters

        Raises:
            ResourceNotFoundException: If resource not found
            ParameterNotFoundException: If no data found for resource/geoid
        """
        # Convert resource to commodity
        commodity = UsdaCensusService._get_commodity_by_resource(session, resource)

        # Get all observations
        observations = UsdaCensusService._get_observations_for_census_record(
            session, commodity.id, geoid
        )

        if not observations:
            raise ParameterNotFoundException(
                "any parameter",
                f"resource {resource} in geoid {geoid}"
            )

        return {
            "usda_crop": None,
            "resource": resource,
            "geoid": geoid,
            "data": observations,
        }
