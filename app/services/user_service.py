import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session

from app.core.messages.error_message import ErrorMessages
from app.core.messages.success_message import SuccessMessages
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.repositories.user import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_users_with_count,
    soft_delete_user,
    update_user,
)
from app.schemas.user import UserCreate, UsersPublic, UserUpdate


def delete_own_account_service(
    session: Session, current_user: User, password: str
) -> dict[str, Any]:
    """
    Securely delete own account with password confirmation.
    Uses soft delete.
    """
    if not verify_password(password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessages.INVALID_PASSWORD,
        )
    soft_delete_user(session, current_user)
    return {"success": True, "message": SuccessMessages.USER_DELETED}


def delete_user_service(session: Session, user_id: uuid.UUID) -> dict[str, Any]:
    """Admin-level soft delete for any user."""
    db_user = get_user_service(session, user_id)
    soft_delete_user(session, db_user)
    return {"success": True, "message": SuccessMessages.USER_DELETED}


def create_user_service(session: Session, user_create: UserCreate) -> User:
    """
    Business logic to create a new user.
    Checks for email availability and hashes the password.
    """
    # 1. Guard check: Email must be unique
    existing_user = get_user_by_email(session, email=user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ErrorMessages.EMAIL_ALREADY_EXISTS,
        )

    # 2. Prepare user object
    user_data = user_create.model_dump(exclude={"password"})
    db_obj = User.model_validate(
        user_data,
        update={"hashed_password": get_password_hash(user_create.password)},
    )

    # 3. Call repository
    return create_user(session, db_obj)


def get_user_service(session: Session, user_id: uuid.UUID) -> User:
    """Get a user by ID or raise 404."""
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
    return user


def list_users_service(
    session: Session, skip: int = 0, limit: int = 100
) -> UsersPublic:
    """List users with pagination count."""
    users, count = get_users_with_count(session, skip=skip, limit=limit)
    return UsersPublic(data=users, count=count)


def update_user_service(
    session: Session, user_id: uuid.UUID, user_update: UserUpdate
) -> User:
    """Update user information including password hashing if provided."""
    db_user = get_user_service(session, user_id)

    # 1. Check email uniqueness if email is being updated
    if user_update.email and user_update.email != db_user.email:
        existing_user = get_user_by_email(session, email=user_update.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.EMAIL_ALREADY_EXISTS,
            )

    # 2. Prepare update data
    update_dict = user_update.model_dump(exclude_unset=True)
    if "password" in update_dict:
        password = update_dict.pop("password")
        update_dict["hashed_password"] = get_password_hash(password)

    # 3. Call repository
    return update_user(session, db_user, update_dict)
