"""Primary product CRUD endpoints.

This module provides REST API endpoints for primary product operations.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from ca_biositing.datamodels.biomass import PrimaryProduct
from ca_biositing.webservice.dependencies import PaginationDep, SessionDep
from ca_biositing.webservice.schemas.common import (
    MessageResponse,
    PaginatedResponse,
    PaginationInfo,
)
from ca_biositing.webservice.schemas.products import (
    PrimaryProductCreate,
    PrimaryProductResponse,
    PrimaryProductUpdate,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "",
    response_model=PaginatedResponse[PrimaryProductResponse],
    status_code=status.HTTP_200_OK,
    summary="List products",
    description="Get a paginated list of all primary products",
)
def list_products(
    session: SessionDep,
    pagination: PaginationDep,
) -> PaginatedResponse[PrimaryProductResponse]:
    """Get a paginated list of primary products.
    
    Args:
        session: Database session
        pagination: Pagination parameters
        
    Returns:
        Paginated response with products
    """
    # Get total count
    count_statement = select(PrimaryProduct)
    total = len(session.exec(count_statement).all())
    
    # Get paginated results
    statement = select(PrimaryProduct).offset(pagination.skip).limit(pagination.limit)
    products = session.exec(statement).all()
    
    return PaginatedResponse(
        items=[PrimaryProductResponse.model_validate(p) for p in products],
        pagination=PaginationInfo(
            total=total,
            skip=pagination.skip,
            limit=pagination.limit,
            returned=len(products),
        ),
    )


@router.get(
    "/{product_id}",
    response_model=PrimaryProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Get product by ID",
    description="Get a specific primary product by its ID",
)
def get_product(product_id: int, session: SessionDep) -> PrimaryProductResponse:
    """Get a specific primary product by ID.
    
    Args:
        product_id: ID of the product to retrieve
        session: Database session
        
    Returns:
        Primary product entry
        
    Raises:
        HTTPException: If product not found
    """
    product = session.get(PrimaryProduct, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return PrimaryProductResponse.model_validate(product)


@router.post(
    "",
    response_model=PrimaryProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
    description="Create a new primary product",
)
def create_product(
    product_data: PrimaryProductCreate,
    session: SessionDep,
) -> PrimaryProductResponse:
    """Create a new primary product.
    
    Args:
        product_data: Product data to create
        session: Database session
        
    Returns:
        Created primary product
    """
    product = PrimaryProduct(**product_data.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)
    return PrimaryProductResponse.model_validate(product)


@router.put(
    "/{product_id}",
    response_model=PrimaryProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update product",
    description="Update an existing primary product",
)
def update_product(
    product_id: int,
    product_data: PrimaryProductUpdate,
    session: SessionDep,
) -> PrimaryProductResponse:
    """Update an existing primary product.
    
    Args:
        product_id: ID of the product to update
        product_data: Updated product data
        session: Database session
        
    Returns:
        Updated primary product
        
    Raises:
        HTTPException: If product not found
    """
    product = session.get(PrimaryProduct, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return PrimaryProductResponse.model_validate(product)


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete product",
    description="Delete a primary product",
)
def delete_product(product_id: int, session: SessionDep) -> MessageResponse:
    """Delete a primary product.
    
    Args:
        product_id: ID of the product to delete
        session: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If product not found
    """
    product = session.get(PrimaryProduct, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    
    session.delete(product)
    session.commit()
    return MessageResponse(message=f"Product {product_id} deleted successfully")
