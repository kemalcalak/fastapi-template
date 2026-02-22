import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel


class ActivityType(str, Enum):
    """Types of activities that can be logged."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    LOGIN = "login"
    LOGOUT = "logout"
    EXPORT = "export"
    INVITE = "invite"


class ResourceType(str, Enum):
    """Types of resources that activities can be performed on."""

    USER = "user"
    AUTH = "auth"


class ActivityStatus(str, Enum):
    """Status of the activity."""

    SUCCESS = "success"
    FAILURE = "failure"


class UserActivityCreate(BaseModel):
    """Schema for creating a user activity log."""

    user_id: uuid.UUID
    activity_type: ActivityType
    resource_type: ResourceType
    resource_id: uuid.UUID | None = None
    details: dict[str, Any] = {}
    status: ActivityStatus = ActivityStatus.SUCCESS
    ip_address: str | None = None
    user_agent: str | None = None
