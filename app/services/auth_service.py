from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.messages.error_message import ErrorMessages
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user import get_user_by_email
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.user_service import create_user_service


def register_service(session: Session, user_create: UserCreate) -> User:
    """
    Handle public user registration.
    Orchestrates user creation and any post-registration tasks.
    """
    return create_user_service(session, user_create)


def authenticate(session: Session, email: str, password: str) -> Any:
    """
    Authenticate a user by email and password.
    Returns the user object if successful, raises 401 otherwise.
    Combined check for security (timing attacks).
    """
    user = get_user_by_email(session, email=email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_PASSWORD,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessages.USER_INACTIVE,
        )

    return user


def login_service(session: Session, email: str, password: str) -> Token:
    """
    Orchestrate the login process: authenticate user and generate JWT tokens.
    Simplified token creation relying on security component defaults.
    """
    user = authenticate(session, email=email, password=password)

    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )
