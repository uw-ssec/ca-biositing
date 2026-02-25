"""Authentication endpoints: login, register, refresh, logout."""

from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from ca_biositing.datamodels.models import ApiUser
from ca_biositing.webservice.config import config
from ca_biositing.webservice.dependencies import AdminUserDep, CurrentUserDep, SessionDep
from ca_biositing.webservice.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from ca_biositing.webservice.v1.auth.schemas import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

_CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


def _set_access_cookie(response: Response, token: str, secure: bool) -> None:
    """Set the HTTP-only access_token cookie on the response."""
    max_age = config.jwt_expire_minutes * 60
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=max_age,
        httponly=True,
        secure=secure,
        samesite="lax",
        path="/",
    )


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SessionDep = ...,
    response: Response = ...,
) -> Token:
    """Authenticate with username/password and receive a JWT access token.

    Also sets an HTTP-only `access_token` cookie for browser SPA clients.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise _CREDENTIALS_ERROR

    expires = timedelta(minutes=config.jwt_expire_minutes)
    token = create_access_token(
        {"sub": user.username},
        config.jwt_secret_key,
        config.jwt_algorithm,
        expires,
    )
    _set_access_cookie(response, token, config.jwt_cookie_secure)
    return Token(access_token=token, token_type="bearer")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_create: UserCreate,
    session: SessionDep,
    _admin: AdminUserDep,
) -> UserResponse:
    """Create a new API user. Requires admin privileges."""
    existing = session.exec(
        select(ApiUser).where(ApiUser.username == user_create.username)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user_create.username}' already exists",
        )

    new_user = ApiUser(
        username=user_create.username,
        hashed_password=get_password_hash(user_create.password),
        email=user_create.email,
        full_name=user_create.full_name,
        is_admin=user_create.is_admin,
        disabled=False,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        is_admin=new_user.is_admin,
        disabled=new_user.disabled,
    )


@router.post("/refresh", response_model=Token)
def refresh(
    current_user: CurrentUserDep,
    response: Response,
) -> Token:
    """Issue a new access token for the currently authenticated user.

    Requires a valid (non-expired) token via Bearer header or cookie.
    Also updates the HTTP-only cookie with the new token.
    """
    expires = timedelta(minutes=config.jwt_expire_minutes)
    token = create_access_token(
        {"sub": current_user.username},
        config.jwt_secret_key,
        config.jwt_algorithm,
        expires,
    )
    _set_access_cookie(response, token, config.jwt_cookie_secure)
    return Token(access_token=token, token_type="bearer")


@router.post("/logout")
def logout(response: Response) -> dict:
    """Clear the access_token cookie, effectively logging out browser clients.

    Note: the JWT itself remains valid until expiry. Bearer-token clients should
    discard the token client-side. Only the HTTP-only cookie is cleared here.
    """
    response.delete_cookie(key="access_token", path="/")
    return {"message": "Logged out"}
