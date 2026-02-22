import uuid
from collections.abc import Sequence

from sqlmodel import Session, func, select

from app.models.user import User
from app.utils import utc_now


def get_user_by_id(session: Session, user_id: uuid.UUID) -> User | None:
    """Get a single user by their UUID. Excludes deleted users."""
    user = session.get(User, user_id)
    if user and user.is_deleted:
        return None
    return user


def get_user_by_email(session: Session, email: str) -> User | None:
    """Get a single user by their email address. Excludes deleted users."""
    statement = (
        select(User).where(User.email == email).where(User.is_deleted.is_(False))
    )
    return session.exec(statement).first()


def get_users_with_count(
    session: Session, skip: int = 0, limit: int = 100
) -> tuple[Sequence[User], int]:
    """Get paginated users and total count. Excludes deleted users."""
    count_statement = (
        select(func.count()).select_from(User).where(User.is_deleted.is_(False))
    )
    count = session.exec(count_statement).one()

    users_statement = (
        select(User).where(User.is_deleted.is_(False)).offset(skip).limit(limit)
    )
    users = session.exec(users_statement).all()
    return users, count


def create_user(session: Session, user: User) -> User:
    """Create a new user in the database."""
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, db_user: User, update_data: dict) -> User:
    """Update an existing user's data."""
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def soft_delete_user(session: Session, user: User) -> None:
    """Mark a user as deleted without physical removal."""
    user.is_deleted = True
    user.deleted_at = utc_now()
    user.is_active = False
    session.add(user)
    session.commit()


def delete_user(session: Session, db_user: User) -> None:
    """Delete a user from the database."""
    session.delete(db_user)
    session.commit()
