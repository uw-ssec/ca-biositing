"""Service layer for USDA Survey data operations.

This module provides business logic for querying USDA survey data
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
from ca_biositing.webservice.services._usda_lookup_common import get_commodity_by_name
from ca_biositing.webservice.exceptions import (
    ParameterNotFoundException,
    ResourceNotFoundException,
)
from ca_biositing.webservice.services._canonical_views import get_usda_survey_view


class UsdaSurveyService:
    """Business logic for USDA Survey data operations."""

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
    def _get_observations_for_survey_record(
        session: Session,
        commodity_id: int,
        geoid: str,
        parameter_name: Optional[str] = None
    ) -> tuple[list[dict], Optional[dict]]:
        """Get observations for a survey record by commodity and geoid.

        Args:
            session: Database session
            commodity_id: USDA commodity ID
            geoid: Geographic identifier
            parameter_name: Optional parameter name filter

        Returns:
            Tuple of (list of observation dictionaries, survey metadata)
        """
        survey_view = get_usda_survey_view(session)

        latest_record_stmt = (
            select(survey_view.c.source_record_id)
            .where(and_(
                survey_view.c.commodity_id == commodity_id,
                survey_view.c.geoid == geoid,
            ))
            .order_by(
                survey_view.c.record_year.desc(),
                survey_view.c.source_record_id.desc(),
            )
            .limit(1)
        )
        latest_record_id = session.execute(latest_record_stmt).scalar_one_or_none()

        if latest_record_id is None:
            return [], None

        stmt = (
            select(
                survey_view.c.id,
                survey_view.c.parameter,
                survey_view.c.value,
                survey_view.c.unit,
                survey_view.c.dimension,
                survey_view.c.dimension_value,
                survey_view.c.dimension_unit,
                survey_view.c.survey_program_id,
                survey_view.c.survey_period,
                survey_view.c.reference_month,
                survey_view.c.seasonal_flag,
            )
            .where(and_(
                survey_view.c.commodity_id == commodity_id,
                survey_view.c.geoid == geoid,
                survey_view.c.source_record_id == latest_record_id,
            ))
        )

        if parameter_name:
            stmt = stmt.where(survey_view.c.parameter == parameter_name)

        # Order by observation ID for deterministic results
        stmt = stmt.order_by(survey_view.c.id)

        results = session.execute(stmt).all()

        observations = []
        survey_metadata: Optional[dict] = None
        for row in results:
            if survey_metadata is None:
                survey_metadata = {
                    "survey_program_id": row.survey_program_id,
                    "survey_period": row.survey_period,
                    "reference_month": row.reference_month,
                    "seasonal_flag": row.seasonal_flag,
                }
            observations.append({
                "parameter": row.parameter,
                "value": float(row.value) if row.value is not None else None,
                "unit": row.unit,
                "dimension": row.dimension,
                "dimension_value": float(row.dimension_value)
                if row.dimension_value is not None else None,
                "dimension_unit": row.dimension_unit,
            })

        return observations, survey_metadata

    @staticmethod
    def get_by_crop(
        session: Session,
        usda_crop: str,
        geoid: str,
        parameter: str
    ) -> dict:
        """Get single survey parameter by crop name.

        Args:
            session: Database session
            usda_crop: USDA crop name
            geoid: Geographic identifier
            parameter: Parameter name

        Returns:
            Dictionary with survey data

        Raises:
            CropNotFoundException: If crop not found
            ParameterNotFoundException: If parameter not found for crop/geoid
        """
        # Validate crop exists
        commodity = UsdaSurveyService._get_commodity_by_name(session, usda_crop)

        # Get observations and survey record
        observations, survey_metadata = UsdaSurveyService._get_observations_for_survey_record(
            session, commodity.id, geoid, parameter
        )

        if not observations or not survey_metadata:
            raise ParameterNotFoundException(
                parameter,
                f"crop {usda_crop} in geoid {geoid}"
            )

        # Return first observation with metadata and survey-specific fields
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
            "survey_program_id": survey_metadata["survey_program_id"],
            "survey_period": survey_metadata["survey_period"],
            "reference_month": survey_metadata["reference_month"],
            "seasonal_flag": survey_metadata["seasonal_flag"],
        }

    @staticmethod
    def get_by_resource(
        session: Session,
        resource: str,
        geoid: str,
        parameter: str
    ) -> dict:
        """Get single survey parameter by resource name.

        Args:
            session: Database session
            resource: Resource name
            geoid: Geographic identifier
            parameter: Parameter name

        Returns:
            Dictionary with survey data

        Raises:
            ResourceNotFoundException: If resource not found
            ParameterNotFoundException: If parameter not found for resource/geoid
        """
        # Convert resource to commodity
        commodity = UsdaSurveyService._get_commodity_by_resource(session, resource)

        # Get observations and survey record
        observations, survey_metadata = UsdaSurveyService._get_observations_for_survey_record(
            session, commodity.id, geoid, parameter
        )

        if not observations or not survey_metadata:
            raise ParameterNotFoundException(
                parameter,
                f"resource {resource} in geoid {geoid}"
            )

        # Return first observation with metadata and survey-specific fields
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
            "survey_program_id": survey_metadata["survey_program_id"],
            "survey_period": survey_metadata["survey_period"],
            "reference_month": survey_metadata["reference_month"],
            "seasonal_flag": survey_metadata["seasonal_flag"],
        }

    @staticmethod
    def list_by_crop(
        session: Session,
        usda_crop: str,
        geoid: str
    ) -> dict:
        """List all survey parameters for crop/geoid.

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
        commodity = UsdaSurveyService._get_commodity_by_name(session, usda_crop)

        # Get all observations and survey record
        observations, survey_metadata = UsdaSurveyService._get_observations_for_survey_record(
            session, commodity.id, geoid
        )

        if not observations or not survey_metadata:
            raise ParameterNotFoundException(
                "any parameter",
                f"crop {usda_crop} in geoid {geoid}"
            )

        return {
            "usda_crop": usda_crop,
            "resource": None,
            "geoid": geoid,
            "data": observations,
            "survey_program_id": survey_metadata["survey_program_id"],
            "survey_period": survey_metadata["survey_period"],
            "reference_month": survey_metadata["reference_month"],
            "seasonal_flag": survey_metadata["seasonal_flag"],
        }

    @staticmethod
    def list_by_resource(
        session: Session,
        resource: str,
        geoid: str
    ) -> dict:
        """List all survey parameters for resource/geoid.

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
        commodity = UsdaSurveyService._get_commodity_by_resource(session, resource)

        # Get all observations and survey record
        observations, survey_metadata = UsdaSurveyService._get_observations_for_survey_record(
            session, commodity.id, geoid
        )

        if not observations or not survey_metadata:
            raise ParameterNotFoundException(
                "any parameter",
                f"resource {resource} in geoid {geoid}"
            )

        return {
            "usda_crop": None,
            "resource": resource,
            "geoid": geoid,
            "data": observations,
            "survey_program_id": survey_metadata["survey_program_id"],
            "survey_period": survey_metadata["survey_period"],
            "reference_month": survey_metadata["reference_month"],
            "seasonal_flag": survey_metadata["seasonal_flag"],
        }
