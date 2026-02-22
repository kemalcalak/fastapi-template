import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr

if TYPE_CHECKING:
    from app.models.user_activity import UserActivity
from sqlmodel import Field, Relationship, SQLModel

from app.utils import utc_now


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    title: str | None = Field(default=None, max_length=100)
    role: str = Field(default="user", max_length=20)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    is_deleted: bool = Field(default=False, index=True)
    deleted_at: datetime | None = Field(default=None)

    activities: list["UserActivity"] = Relationship(back_populates="user")
