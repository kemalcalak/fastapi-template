import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import Column, String

if TYPE_CHECKING:
    from app.models.user import User
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import Field, Relationship, SQLModel

from app.schemas.user_activity import ActivityStatus
from app.utils import utc_now


class UserActivity(SQLModel, table=True):
    """
    Model to track user activities and audit logs.
    """

    __tablename__ = "user_activity"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(PG_UUID(as_uuid=True), primary_key=True),
    )

    user_id: uuid.UUID = Field(foreign_key="user.id", index=True, nullable=False)

    # Enums stored as strings
    activity_type: str = Field(sa_column=Column(String, nullable=False, index=True))
    resource_type: str = Field(sa_column=Column(String, nullable=False, index=True))

    resource_id: uuid.UUID | None = Field(
        default=None, sa_column=Column(PG_UUID(as_uuid=True), nullable=True, index=True)
    )

    details: dict[str, Any] = Field(default={}, sa_column=Column(JSON, nullable=False))

    status: str = Field(
        default=ActivityStatus.SUCCESS.value, sa_column=Column(String, nullable=False)
    )

    ip_address: str | None = Field(default=None, nullable=True)
    user_agent: str | None = Field(default=None, nullable=True)

    created_at: datetime = Field(default_factory=utc_now, nullable=False, index=True)

    # Relationships
    user: "User" = Relationship(back_populates="activities")

    class Config:
        use_enum_values = True
