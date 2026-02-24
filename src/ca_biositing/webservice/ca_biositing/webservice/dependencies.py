"""Dependencies for FastAPI endpoints.

This module provides dependency injection functions for database sessions,
authentication, and common query parameters.
"""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ca_biositing.datamodels.database import get_session
from ca_biositing.datamodels.models import ApiUser
from ca_biositing.webservice.config import config
from ca_biositing.webservice.services.auth_service import decode_access_token


# Database session dependency
SessionDep = Annotated[Session, Depends(get_session)]


def pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
):
    """Common pagination parameters for list endpoints."""
    return {"skip": skip, "limit": limit}


# Pagination dependency
PaginationDep = Annotated[dict, Depends(pagination_params)]


# OAuth2 scheme — auto_error=False allows cookie fallback when Bearer is missing
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token", auto_error=False)


def get_current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    request: Request,
    session: SessionDep,
) -> ApiUser:
    """Resolve the current authenticated user from Bearer token or HTTP-only cookie.

    Checks the Authorization: Bearer header first; if absent, falls back to the
    access_token cookie. Raises 401 if no valid token is found or the user is disabled.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Prefer Bearer header; fall back to cookie
    resolved_token: Optional[str] = token or request.cookies.get("access_token")
    if not resolved_token:
        raise credentials_exception

    username = decode_access_token(
        resolved_token,
        config.jwt_secret_key,
        config.jwt_algorithm,
    )
    if not username:
        raise credentials_exception

    user = session.exec(select(ApiUser).where(ApiUser.username == username)).first()
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
        )
    return user


# Typed dependency aliases
CurrentUserDep = Annotated[ApiUser, Depends(get_current_user)]


def get_current_admin_user(current_user: CurrentUserDep) -> ApiUser:
    """Require the current user to be an admin. Raises 403 otherwise."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


AdminUserDep = Annotated[ApiUser, Depends(get_current_admin_user)]
