"""Dependencies for FastAPI endpoints.

This module provides dependency injection functions for database sessions,
authentication, and common query parameters.
"""

from __future__ import annotations

from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, Query, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ca_biositing.datamodels.database import get_session
from ca_biositing.datamodels.models import ApiKey, ApiUser
from ca_biositing.webservice.config import config
from ca_biositing.webservice.services.auth_service import (
    check_and_increment_rate_limit,
    decode_access_token,
    validate_api_key,
)


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
    x_api_key: Annotated[Optional[str], Header(alias="X-API-Key")] = None,
) -> ApiUser:
    """Resolve the current authenticated user.

    Auth check order:
    1. Authorization: Bearer <jwt> header
    2. access_token HTTP-only cookie
    3. X-API-Key header (per-client API key with rate limiting)

    Raises 401 if no valid credential is found or the user is disabled.
    Raises 429 if the API key's rate limit is exceeded.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # --- Path 1 & 2: JWT (Bearer header or cookie) ---
    resolved_token: Optional[str] = token or request.cookies.get("access_token")
    if resolved_token:
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

    # --- Path 3: X-API-Key header ---
    if x_api_key:
        api_key = validate_api_key(session, x_api_key)
        if not api_key:
            raise credentials_exception
        user = session.exec(select(ApiUser).where(ApiUser.id == api_key.api_user_id)).first()
        if user is None or user.disabled:
            raise credentials_exception
        if not check_and_increment_rate_limit(session, api_key):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
                headers={"Retry-After": "60"},
            )
        return user

    raise credentials_exception


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
