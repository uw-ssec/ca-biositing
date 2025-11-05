"""Business logic for experiment operations.

This module provides service functions for experiment CRUD operations.
"""

from __future__ import annotations

from typing import List, Optional

from sqlmodel import Session, select

from ca_biositing.datamodels.experiments_analysis import Experiment
from ca_biositing.webservice.schemas.experiments import ExperimentCreate, ExperimentUpdate


def get_experiment_list(
    session: Session,
    skip: int = 0,
    limit: int = 50,
) -> tuple[List[Experiment], int]:
    """Get a list of experiments with pagination.
    
    Args:
        session: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        Tuple of (list of experiments, total count)
    """
    # Get total count
    count_statement = select(Experiment)
    total = len(session.exec(count_statement).all())
    
    # Get paginated results
    statement = select(Experiment).offset(skip).limit(limit)
    experiments = session.exec(statement).all()
    
    return list(experiments), total


def get_experiment_by_id(session: Session, experiment_id: int) -> Optional[Experiment]:
    """Get an experiment by ID.
    
    Args:
        session: Database session
        experiment_id: Experiment ID to retrieve
        
    Returns:
        Experiment or None if not found
    """
    return session.get(Experiment, experiment_id)


def create_experiment(session: Session, experiment_data: ExperimentCreate) -> Experiment:
    """Create a new experiment.
    
    Args:
        session: Database session
        experiment_data: Experiment data to create
        
    Returns:
        Created experiment
    """
    experiment = Experiment(**experiment_data.model_dump())
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    return experiment


def update_experiment(
    session: Session,
    experiment_id: int,
    experiment_data: ExperimentUpdate,
) -> Optional[Experiment]:
    """Update an existing experiment.
    
    Args:
        session: Database session
        experiment_id: Experiment ID to update
        experiment_data: Updated experiment data
        
    Returns:
        Updated experiment or None if not found
    """
    experiment = session.get(Experiment, experiment_id)
    if not experiment:
        return None
    
    # Update only provided fields
    update_data = experiment_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(experiment, key, value)
    
    session.add(experiment)
    session.commit()
    session.refresh(experiment)
    return experiment


def delete_experiment(session: Session, experiment_id: int) -> bool:
    """Delete an experiment.
    
    Args:
        session: Database session
        experiment_id: Experiment ID to delete
        
    Returns:
        True if deleted, False if not found
    """
    experiment = session.get(Experiment, experiment_id)
    if not experiment:
        return False
    
    session.delete(experiment)
    session.commit()
    return True
