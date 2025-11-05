"""Business logic for biomass operations.

This module provides service functions for biomass CRUD operations.
"""

from __future__ import annotations

from typing import List, Optional

from sqlmodel import Session, select

from ca_biositing.datamodels.biomass import Biomass
from ca_biositing.webservice.schemas.biomass import BiomassCreate, BiomassUpdate


def get_biomass_list(
    session: Session,
    skip: int = 0,
    limit: int = 50,
) -> tuple[List[Biomass], int]:
    """Get a list of biomass entries with pagination.

    Args:
        session: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        Tuple of (list of biomass entries, total count)
    """
    # Get total count
    count_statement = select(Biomass)
    total = len(session.exec(count_statement).all())

    # Get paginated results
    statement = select(Biomass).offset(skip).limit(limit)
    biomass_list = session.exec(statement).all()

    return list(biomass_list), total


def get_biomass_by_id(session: Session, biomass_id: int) -> Optional[Biomass]:
    """Get a biomass entry by ID.

    Args:
        session: Database session
        biomass_id: Biomass ID to retrieve

    Returns:
        Biomass entry or None if not found
    """
    return session.get(Biomass, biomass_id)


def create_biomass(session: Session, biomass_data: BiomassCreate) -> Biomass:
    """Create a new biomass entry.

    Args:
        session: Database session
        biomass_data: Biomass data to create

    Returns:
        Created biomass entry
    """
    biomass = Biomass(**biomass_data.model_dump())
    session.add(biomass)
    session.commit()
    session.refresh(biomass)
    return biomass


def update_biomass(
    session: Session,
    biomass_id: int,
    biomass_data: BiomassUpdate,
) -> Optional[Biomass]:
    """Update an existing biomass entry.

    Args:
        session: Database session
        biomass_id: Biomass ID to update
        biomass_data: Updated biomass data

    Returns:
        Updated biomass entry or None if not found
    """
    biomass = session.get(Biomass, biomass_id)
    if not biomass:
        return None

    # Update only provided fields
    update_data = biomass_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(biomass, key, value)

    session.add(biomass)
    session.commit()
    session.refresh(biomass)
    return biomass


def delete_biomass(session: Session, biomass_id: int) -> bool:
    """Delete a biomass entry.

    Args:
        session: Database session
        biomass_id: Biomass ID to delete

    Returns:
        True if deleted, False if not found
    """
    biomass = session.get(Biomass, biomass_id)
    if not biomass:
        return False

    session.delete(biomass)
    session.commit()
    return True
